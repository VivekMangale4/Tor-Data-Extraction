import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd

# Create a Tor session with retry
def create_session_with_retry():
    session = requests.session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9051'
    }
    return session

# Fetch .onion content
def fetch_onion_content(url, session):
    try:
        response = session.get(url, timeout=60)  # Increased timeout
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Extract metadata
def extract_metadata(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {
        'title': soup.title.string if soup.title else 'N/A',
        'headers': [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
    }
    return metadata

# Identify sensitive info
def identify_sensitive_info(html_content):
    sensitive_info = []
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ip_matches = ip_pattern.findall(html_content)
    
    if ip_matches:
        sensitive_info.append(f"IP Leak Detected: {', '.join(ip_matches)}")
    
    if "X-Forwarded-For" in html_content:
        sensitive_info.append("X-Forwarded-For header detected")
    
    return sensitive_info

# Extract external resources
def extract_external_resources(html_content):
    external_resources = []
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(['a', 'img', 'script', 'link']):
        if tag.get('href'):
            external_resources.append(tag['href'])
        elif tag.get('src'):
            external_resources.append(tag['src'])
    return external_resources

# Monitor response headers
def monitor_response_headers(response):
    headers_info = []
    if 'X-Powered-By' in response.headers:
        headers_info.append(f"X-Powered-By: {response.headers['X-Powered-By']}")
    if 'Server' in response.headers:
        headers_info.append(f"Server: {response.headers['Server']}")
    return headers_info

# Store data in SQLite and display table format
def store_and_display_data(url, metadata, sensitive_info, external_resources, headers_info):
    conn = sqlite3.connect('extracted_data.db')
    c = conn.cursor()
    
    # Create a new table extractiono
    c.execute('''CREATE TABLE IF NOT EXISTS extractiono (
                    url TEXT,
                    title TEXT,
                    headers TEXT,
                    sensitive_info TEXT,
                    external_resources TEXT,
                    headers_info TEXT
                )''')
    
    headers = ', '.join(metadata['headers']) if metadata['headers'] else 'None'
    sensitive_info_str = ', '.join(sensitive_info) if sensitive_info else 'None'
    external_resources_str = ', '.join(external_resources) if external_resources else 'None'
    headers_info_str = ', '.join(headers_info) if headers_info else 'None'
    
    c.execute('''INSERT INTO extractiono (url, title, headers, sensitive_info, external_resources, headers_info) 
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (url, metadata['title'], headers, sensitive_info_str, external_resources_str, headers_info_str))
    
    conn.commit()
    
    # Fetch and display data in table format using pandas
    df = pd.read_sql_query("SELECT * FROM extractiono", conn)
    print("\nExtracted Data in Table Format:")
    print(df)
    
    conn.close()

# Example usage
onion_url = "http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion/"
session = create_session_with_retry()
response = fetch_onion_content(onion_url, session)

if response:
    html_content = response.text
    metadata = extract_metadata(html_content)
    sensitive_info = identify_sensitive_info(html_content)
    external_resources = extract_external_resources(html_content)
    headers_info = monitor_response_headers(response)
    
    store_and_display_data(onion_url, metadata, sensitive_info, external_resources, headers_info)
else:
    print("Failed to fetch content.")

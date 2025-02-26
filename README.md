# TOR Data Extraction 🚀  

## **Overview**  
The **Tor network** provides anonymity by routing traffic through multiple encrypted relays. However, security researchers and forensic analysts often require **insight into hidden services (.onion sites)** for **threat intelligence, OSINT, and cybersecurity investigations**.  

This project automates **.onion site data extraction and analysis** using Python and SQLite.  

---

## **Features**  
🔍 **Extract data from .onion websites**  
🔗 **Crawl and scrape publicly available content**  
🗂 **Store extracted data in SQLite database**  
📊 **Analyze extracted data using built-in tools**  

---

## **Installation & Setup**  

### **Prerequisites**  
Ensure **Tor Browser** is installed and running.  

### **Install Tor on Kali Linux**  
Run the following commands in the Kali Linux terminal:  

```bash
sudo apt update && sudo apt install tor torbrowser-launcher
```

### **Start Tor Service**  
Before running the script, start the **Tor service**:  

```bash
torbrowser-launcher  # Launch Tor browser manually (optional)
sudo systemctl start tor  # Start Tor service
sudo systemctl status tor  # Check if Tor service is active
```

### **Clone and Install Dependencies**  
```bash
git clone https://github.com/your-username/tor-data-extractor.git  
cd tor-data-extractor  
pip install -r requirements.txt  
```

---

## **Usage**  

### **Step 1: Extract Data from .onion Site**  
Run the `script1.py` file to fetch and store data in SQLite:  

```bash
python script1.py
```
📌 This script **connects to a given .onion URL**, scrapes data, and stores it in a local SQLite database.  

### **Step 2: Analyze Extracted Data**  
Run `fetch_table.py` to view and analyze the stored data:  

```bash
python fetch_table.py
```
📌 This script **retrieves data from the SQLite database** and presents it in a readable format.  

---

## **How It Works**  

1. **script1.py**  
   - Connects to the **Tor network** using SOCKS5 proxy (`127.0.0.1:9050`).  
   - Fetches the target `.onion` website's content.  
   - Extracts relevant **metadata, links, Sensitive Info, and other data**.  
   - Stores the extracted data in a **SQLite database**.  

2. **fetch_table.py**  
   - Loads and displays stored data in a **structured tabular format**.  
   - Allows further **analysis of extracted content**.  


## **Configuration**  
To change the target `.onion` website, modify `script1.py`:  

```python
target_url = "http://example.onion"
```

To change the database name, update `fetch_table.py`:  

```python
conn = sqlite3.connect("extracted_data.db")
```

---

## **Ethical Disclaimer ⚠️**  
This project is strictly for **educational** and **legal research purposes only**.  
- Do **NOT** use this tool to access illegal content.  
- The author is **not responsible** for any misuse of this project.  
- Always follow **legal frameworks** and obtain proper authorization before using this tool.  

---

## **Contributing**  
Contributions are welcome! Submit a **pull request** or open an **issue** if you have improvements.  

---

## **License**  
📜 This project is licensed under the **MIT License** – feel free to modify and share responsibly.  

---

## **References & Acknowledgments**  
- [Tor Project](https://www.torproject.org/)  
- [SQLite Documentation](https://sqlite.org/)  
- [OSINT Framework](https://osintframework.com/)  

---

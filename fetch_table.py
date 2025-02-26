import sqlite3
from prettytable import PrettyTable

# Connect to SQLite database
conn = sqlite3.connect('extracted_data.db')  # replace with your database name
cursor = conn.cursor()

# Execute a query to fetch data from a table
cursor.execute("SELECT * FROM extractiono")  # replace with your table name
rows = cursor.fetchall()

# Create a PrettyTable instance
table = PrettyTable()

# Get column names from the cursor description
columns = [description[0] for description in cursor.description]
table.field_names = columns

# Set max width for each column (optional)
for col in columns:
    table.max_width[col] = 13  # Adjust width for better display (increasing number for wider columns)

# Add rows to the table
for row in rows:
    table.add_row(row)

# Display the table
print(table)

# Close the connection
conn.close()

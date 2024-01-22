import shutil
import sqlite3

# Replace with the actual path to your "History" file
original_history_file = "C:/Users/Barak/AppData/Local/Google/Chrome/User Data/Default/History"
copied_history_file = "copied_history.db"

# Create a copy of the "History" file
shutil.copy(original_history_file, copied_history_file)

# Connect to the copied SQLite database
connection = sqlite3.connect(copied_history_file)
cursor = connection.cursor()

# Execute a query to fetch data from the "urls" table (table that stores browsing history)
cursor.execute("SELECT * FROM urls")

# Fetch all the rows (browsing history entries) from the result set
rows = cursor.fetchall()

# Close the database connection
connection.close()

# Write the browsing history entries to a text file
output_file_path = "browsing_history.txt"  # Replace with your desired output file path

with open(output_file_path, "w", encoding="utf-8") as file:
    for row in rows:
        url = row[1]  # The URL of the visited website is stored in the second column (index 1)
        title = row[2]  # The title of the visited website is stored in the third column (index 2)
        visit_time = row[3]  # The timestamp of the visit is stored in the fourth column (index 3)
        file.write(f"URL: {url}, Title: {title}, Visit Time: {visit_time}\n")

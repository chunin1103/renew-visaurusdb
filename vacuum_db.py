import sqlite3

# Database file path
db_path = './synonyms.db'

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    print("Connected to the database.")

    # Executing the VACUUM command
    conn.execute("VACUUM")
    print("VACUUM operation completed successfully.")

except sqlite3.Error as e:
    print(f"An error occurred during VACUUM: {e}")
finally:
    # Closing the connection
    if conn:
        conn.close()
        print("Database connection closed.")

# You can then check the file size as follows
import os
new_file_size_mb = os.path.getsize(db_path) / (1024 * 1024)
print(f"New database file size: {new_file_size_mb:.2f} MB")
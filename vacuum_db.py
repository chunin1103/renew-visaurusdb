#github-action genshdoc
import sqlite3
import os

def vacuum_database(db_path):
    """
    Performs a VACUUM operation on the specified SQLite database to rebuild it,
    thereby optimizing it and reducing file size.

    Args:
    db_path (str): The file path to the SQLite database.

    Returns:
    float: The new file size of the database in megabytes.
    """
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

    # Calculating the new file size
    new_file_size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"New database file size: {new_file_size_mb:.2f} MB")
    return new_file_size_mb

# Example usage
db_path = './synonyms.db'
new_file_size_mb = vacuum_database(db_path)
print(f"New database file size: {new_file_size_mb:.2f} MB")

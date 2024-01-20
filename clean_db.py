import sqlite3
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
# Path to the SQLite database file
db_path = './synonyms.db'

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    logging.info("Connected to the database.")

    # Check if both tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    if 'symnonyms' in tables:
        # Drop the 'symnonyms' table
        cursor.execute("DROP TABLE verifieddd_synonyms")
        logging.info("Dropped the 'symnonyms' table.")

    if 'verifiedd_synonyms' in tables:
        # Rename 'verifiedd_synonyms' to 'symnonyms'
        cursor.execute("ALTER TABLE verifiedd_synonyms RENAME TO symnonyms")
        logging.info("Renamed 'verifiedd_synonyms' to 'symnonyms'.")
    else:
        logging.warning("The 'verifiedd_synonyms' table does not exist.")

    # Commit changes
    conn.commit()
    logging.info("Changes committed to the database.")

except sqlite3.Error as e:
    logging.error(f"Database error: {e}")
except Exception as e:
    logging.error(f"Exception in _query: {e}")
finally:
    if conn:
        conn.close()
        logging.info("Database connection closed.")
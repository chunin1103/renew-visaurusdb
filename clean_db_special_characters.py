#github-action genshdoc
import sqlite3
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Replace with your database file path
db_path = './synonyms.db'

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    logging.info("Connected to the database.")

    # Update the 'synonyms' column in the 'symnonyms' table
    update_query = """
    UPDATE symnonyms
    SET synonyms = REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(
                                        REPLACE(
                                            REPLACE(
                                                synonyms, '[', ''
                                            ), ']', ''
                                        ), "'", ''
                                    ), '"', ''
                                ), "nan", ''
                            ), "''", ''
                        ), '""', ''
                    )
    """
    cursor.execute(update_query)
    logging.info("Removed special characters from the 'synonyms' column.")

    # Commit changes
    conn.commit()
    logging.info("Changes committed to the database.")

except sqlite3.Error as e:
    logging.error(f"Database error: {e}")
except Exception as e:
    logging.error(f"Exception in query: {e}")
finally:
    if conn:
        conn.close()
        logging.info("Database connection closed.")
import sqlite3
import openai
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import threading
import re


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

# Set up OpenAI API key
openai.api_key = "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"

# Connect to the SQLite database
conn = sqlite3.connect('synonyms.db')
cursor = conn.cursor()

# Create a new table for testing
cursor.execute("""
    CREATE TABLE IF NOT EXISTS verifiedd_synonyms (
        word TEXT PRIMARY KEY,
        synonyms TEXT
    )
""")
conn.commit()

# Global variable to indicate whether all batches have been processed
all_batches_processed = False

# Execute SQL query to fetch the words and synonyms from the table
cursor.execute('SELECT * FROM symnonyms')
word_data = cursor.fetchall()

# Function to create batches
def batch_generator(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Create word batches
word_batches = list(batch_generator(word_data, 2))

# Function to verify synonyms using GPT-3
def verify_synonyms(word, synonyms_list):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "Linguist."},
                {"role": "user", "content": f"Examine and refine the list {synonyms_list} for Vietnamese synonyms of the Vietnamese word \"{word}\". Return the verified synonyms sorted by confidence level from high to low, strictly in this format: 'Verified:[comma-separated-synonyms]'. Exclude the word \"{word}\" itself from the results. The correct synonyms must be in Vietnamese. If none are verified, reply with ['Không tìm thấy']. No additional comments or text allowed."}  
            ]
        )
        output = str(completion.choices[0].message['content']).encode('utf-8')
        output = output.decode('utf-8') 
        # Extract the part after 'Verified:' and split it into a list of synonyms
        if 'Verified:' in output:
            verified_synonyms = output.split('Verified:')[1].strip().split(', ')
            return verified_synonyms

    except Exception as e:
        logging.info(f"Error processing word: {word} - {str(e)}")
        return None


def update_database(word, synonyms):
    local_conn = sqlite3.connect('synonyms.db')
    local_cursor = local_conn.cursor()
    # Execute the SQL command
    local_cursor.execute(
        "INSERT OR REPLACE INTO verifiedd_synonyms (word, synonyms) VALUES (?, ?)",
        (word, ', '.join(synonyms))
    )
    
    # Commit the changes and close the connection
    local_conn.commit()
    local_conn.close()
# Global variable to keep track of the next batch to process
next_batch_index = 41

max_batches = 51  # New global variable to limit the number of batches

# Create an APScheduler instance
scheduler = BlockingScheduler()

def shutdown_scheduler():
    scheduler.shutdown()

# Define a function to process the next batch
def process_next_batch():
    logging.info("process_next_batch called")
    global next_batch_index
    global all_batches_processed  # Access the global variable

    if next_batch_index < len(word_batches) and next_batch_index < max_batches:  # Check if there are more batches to process
        batch = word_batches[next_batch_index]
        logging.info(f"Processing batch {next_batch_index + 1}")
        for word, synonyms_list in batch:
            synonyms_list = synonyms_list.lstrip(', ')  # Removing leading commas and spaces
            synonyms = verify_synonyms(word, synonyms_list)
            if synonyms:
                logging.info(f"Word: {word}, Synonyms: {', '.join(synonyms)}")
                update_database(word, synonyms)  # Update the database with verified synonyms
            else:
                logging.info(f"Error processing word: {word}")
            time.sleep(19)  # 20-second delay between each API call
        next_batch_index += 1  # Increment the batch index for the next run
    else:
        logging.info("All batches processed")
        all_batches_processed = True  # Set the global variable to True
        shutdown_thread = threading.Thread(target=shutdown_scheduler)  # Create a new thread to shut down the scheduler
        shutdown_thread.start()  # Start the new thread


def main():
    # Schedule the process_next_batch function to run at specified intervals
    scheduler.add_job(process_next_batch, 'interval', minutes=1, id='process_next_batch', max_instances=1)

    # Start the scheduler
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass  # Handle keyboard interrupt and system exit gracefully

if __name__ == "__main__":
    main()
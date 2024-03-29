#github-action genshdoc
import sqlite3
import openai
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import threading


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w', encoding='utf-8')

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
word_batches = list(batch_generator(word_data, 41))

# Function to verify synonyms using GPT-3
def verify_synonyms(word, synonyms_list):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Linguist."},
                {"role": "user", "content": f"Examine and refine the following list of potential synonyms for the Vietnamese word \"{word}\": [{synonyms_list}]. The first priority is to verify and sort the synonyms based on their closeness in meaning to the primary word. Ensure all terms are Vietnamese, including those borrowed from other languages but written in the Latin script. Assess each term's relevance as a synonym, considering their meanings and context-specific usage in Vietnamese. If confident, you may also suggest additional Vietnamese synonyms not listed. Exclude the primary word \"{word}\" itself from the final list. Return the refined list in this format: 'Verified:[comma-separated synonyms]'. If no appropriate Vietnamese synonyms are found, reply with ['Không tìm thấy']. No additional comments or text allowed."}  
            ]
        )
        output = str(completion.choices[0].message['content']).encode('utf-8')
        logging.debug(f"API Response: {output}")
        output = output.decode('utf-8') 
        # Extract the part after 'Verified:' and split it into a list of synonyms
        if 'Verified:' in output:
            verified_synonyms = output.split('Verified:')[1].strip().split(', ')
            return verified_synonyms

    except Exception as e:
        logging.exception(f"Error processing word: {word} - {str(e)}")
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
next_batch_index = 325

max_batches = 900  # New global variable to limit the number of batches

# Create an APScheduler instance
scheduler = BlockingScheduler()

def shutdown_scheduler():
    scheduler.shutdown()

# Define a function to process the next batch
def process_next_batch():
    # logging.info("process_next_batch called")
    global next_batch_index
    global all_batches_processed  # Access the global variable

    if next_batch_index < len(word_batches) and next_batch_index < max_batches:  # Check if there are more batches to process
        batch = word_batches[next_batch_index]
        logging.info(f"Processing batch {next_batch_index + 1}")
        for word, synonyms_list in batch:
            synonyms_list = synonyms_list.lstrip(', ')  # Removing leading commas and spaces
            logging.debug(f"Word: {word}, Synonyms List: {synonyms_list}") # Logging synonyms sent for validation
            synonyms = verify_synonyms(word, synonyms_list)
            if synonyms:
                logging.info(f"Word: {word}, Synonyms: {', '.join(synonyms)}") # Logging verified synonyms
                update_database(word, synonyms)  # Update the database with verified synonyms
            else:
                logging.info(f"Error processing word: {word}")
            time.sleep(7)  # 6-second delay between each API call
        next_batch_index += 1  # Increment the batch index for the next run
    else:
        logging.info("All batches processed")
        all_batches_processed = True  # Set the global variable to True
        shutdown_thread = threading.Thread(target=shutdown_scheduler)  # Create a new thread to shut down the scheduler
        shutdown_thread.start()  # Start the new thread


def main():
    # Schedule the process_next_batch function to run at specified intervals
    scheduler.add_job(process_next_batch, 'interval', seconds=15, id='process_next_batch', max_instances=1)

    # Start the scheduler
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass  # Handle keyboard interrupt and system exit gracefully

if __name__ == "__main__":
    main()
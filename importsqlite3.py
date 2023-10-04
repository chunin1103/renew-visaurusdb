import sqlite3
import openai
import time

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


# Execute SQL query to fetch the words and synonyms from the table
cursor.execute('SELECT * FROM symnonyms')
word_data = cursor.fetchall()

# Function to create batches
def batch_generator(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Create word batches
word_batches = list(batch_generator(word_data, 7))

# Function to verify synonyms using GPT-3
def verify_synonyms(word, synonyms_list):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "Linguist."},
                {"role": "user", "content": f"I have a comma-delimited list of words that are potentially synonyms to the Vietnamese word \"{word}\". Could you please filter out the words that are not correct and provide me with a revised list? The original list is as follows: {synonyms_list}"}  
            ]
        )
        output = str(completion.choices[0].message['content']).encode('utf-8')
        return output.decode('utf-8').split(', ')  # Splitting the revised list of synonyms into a list
    except Exception as e:
        print(f"Error processing word: {word} - {str(e)}")
        return None


def update_database(word, synonyms):
    cursor.execute("INSERT OR REPLACE INTO verifiedd_synonyms (word, synonyms) VALUES (?, ?)", (word, ', '.join(synonyms)))
    conn.commit()
# Process the first batch and verify synonyms, then update the database
first_batch = word_batches[1]
print(f"Processing first batch")
for word, synonyms_list in first_batch:
    synonyms_list = synonyms_list.lstrip(', ')  # Removing leading commas and spaces
    synonyms = verify_synonyms(word, synonyms_list)
    if synonyms:
        print(f"Word: {word}, Synonyms: {', '.join(synonyms)}")
        update_database(word, synonyms)  # Update the database with verified synonyms
    else:
        print(f"Error processing word: {word}")
    time.sleep(20)  # 20-second delay between each API call



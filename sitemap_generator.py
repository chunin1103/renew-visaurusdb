import sqlite3

# Database file path
db_path = './synonyms.db'

def extract_words(db_path):
    """ Extract words from the database """
    conn = sqlite3.connect(db_path)  # Connect to the SQLite database
    cur = conn.cursor()  # Create a cursor object

    cur.execute("SELECT word FROM symnonyms;")  # Query to retrieve all words
    words = [word[0] for word in cur.fetchall()]  # Fetch all words and extract from tuples

    cur.close()  # Close the cursor
    conn.close()  # Close the database connection

    return words

def generate_sitemap(words, file_name='sitemap.xml'):
    """ Generate sitemap XML file """
    sitemap_header = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''

    sitemap_footer = '</urlset>'

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(sitemap_header + '\n')
        for word in words:
            word = word.replace(' ', '-')
            file.write(f'  <url>\n    <loc>http://tudiendongnghia.com/search/{word}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n')
        file.write(sitemap_footer)


# Database path
db_path = './synonyms.db'

# Extract words
words_list = extract_words(db_path)

# Generate sitemap
generate_sitemap(words_list)

print("Sitemap generated successfully.")
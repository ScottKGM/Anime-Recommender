import sqlite3

# Name of the database file
DB_NAME = "anime.db"

# 1. Create the anime table if it doesn't exist
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create a table with 8 fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            genres TEXT NOT NULL,
            rating REAL NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT NOT NULL,
            trailer_url TEXT,
            episodes INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# 2. Insert a single anime entry into the table
def insert_anime_batch(anime_list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for anime in anime_list:
        trailer_url = anime.get('trailer', {}).get('url', None)
        cursor.execute('''
            INSERT or IGNORE INTO anime (title, genres, rating, description, image_url, trailer_url, episodes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            anime['title'],
            ', '.join([g['name'] for g in anime['genres']]),
            anime.get('score') or 0,
            anime.get('synopsis') or 'No description available.',
            anime['images']['jpg']['image_url'],
            trailer_url,
            anime.get('episodes') or 0
        ))

    conn.commit()
    conn.close()

#
def query_anime(generes):
    """
    Find anime that contain all genres in the generes list.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Build WHERE clause to require all genres
    where_clause = " OR ".join(["genres LIKE ?"] * len(generes))
    params = [f"%{genre}%" for genre in generes]

    cursor.execute(f'''
        SELECT title, genres, rating, description, image_url 
        FROM anime
        WHERE {where_clause}
    ''', params)

    results = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries for easier processing
    return [{
        'title': row[0],
        'genres': row[1].split(', '),
        'rating': row[2],
        'description': row[3],
        'image_url': row[4]
    } for row in results]
    
    
def get_anime_by_title(title):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT title, genres, rating, description, image_url
        FROM anime
        WHERE title = ?
    ''', (title,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'title': row[0],
            'genres': row[1].split(', '),
            'rating': row[2],
            'description': row[3],
            'image_url': row[4]
        }
    return None


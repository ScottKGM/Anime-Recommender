import requests
import time
from db import create_db, insert_anime_batch

# base API URL
BASE_URL = "https://api.jikan.moe/v4/top/anime"

#Total pages to fetch: 1000 animes
TOTAL_PAGES = 40

def fetch_top_anime():
    create_db()  # Ensure the database is created before inserting data
    total_inserted = 0

    for page in range(1, TOTAL_PAGES + 1):
        print(f"Fetching page {page}/{TOTAL_PAGES}...")
        url = f"{BASE_URL}?page={page}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data= response.json()
            anime_list = data.get('data', [])

            for anime in anime_list:
                insert_anime_batch(anime_list)
                total_inserted +=1

            time.sleep(1)  # Respect API rate limits
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue
    print(f" Done! Inserted: {total_inserted} animes, into anime.db.")

if __name__ == "__main__":
    fetch_top_anime()
    print("All top anime data has been fetched and inserted into the database.")

import requests
from typing import List, Dict
HF_TOKEN = "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"  # Replace with your token
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}  # Replace with your token

def recommend_anime(
        anime_List: List[Dict],
        user_vibe: str,
        num_recommendations: int = 3
) -> str:
    """
    Parameters:
    anime_List: Result from db.query_anime()
    user_vibe: Text description of what user wants
    num_recommendations: Number of anime to recommend
    
    Returns: String with numbered recommendations
    """
    # Format anime data for the AI
    anime_data = []
    for anime in anime_List:
        anime_data.append(
            f"Title: {anime['title']}\n"
            f"Genres: {', '.join(anime['genres'])}\n"
            f"Rating: {anime['rating']}/10\n"
            f"Description: {anime['description'][:200]}...\n"
            "-----"
        )
    
    # Create the AI prompt
    prompt = f"""Analyze these anime and recommend {num_recommendations} that best match:
    
    User Vibe: "{user_vibe}"
    
    Consider:
    - The anime HAS to match the user's vibe
    - Do not be too generic, I want you to find animes that are unique and not mainstream

    
    
    Anime Options:
    {''.join(anime_data)}
    
    Return ONLY the titles as a numbered list like:
    1. First Recommendation
    2. Second Recommendation
    3. Third Recommendation
    """
    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "temperature": .07,
                "max_new_tokens": 200
        }
    },
    )
   




    json_response = response.json()
    print("API Response:", json_response)

    if isinstance(json_response, list) and 'generated_text' in json_response[0]:
        return json_response[0]['generated_text'].strip()
    elif isinstance(json_response, dict) and 'generated_text' in json_response:
        return json_response['generated_text'].strip()
    else:
        print("Unexpected response structure.")
        return "Sorry, I couldn't generate recommendations at the moment."


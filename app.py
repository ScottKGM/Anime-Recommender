import streamlit as st
import requests
import os
import time
from recommender import recommend_anime
from db import get_anime_by_title, query_anime

HF_TOKEN = "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"  # Replace with your token
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}  # Replace with your token

#Set up the prompt
def generate_intro(vibe, generes):
    prompt = f"""
    Imagine you're a passionate anime enthusiast who loves helping friends find new shows. 
    Right now, you're chatting with a friend who says they're feeling "{vibe}" and likes these genres: {', '.join(generes)}.

    Write a friendly, casual 2-3 sentence greeting that:
    - Matches the user's vibe (e.g., emojis for 'hyped', calm tone for 'relaxed')
    - Feels personal and excited
    - Doesn't mention that you're an AI or that this is an app prompt.

    Just write the greeting — no explanations, no extra instructions.
    """

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 60
        }
    },
)

    output= response.json()[0]['generated_text']

    if output.startswith(prompt):
        output = output[len(prompt):]  # Cut off the prompt part

    output = output.strip()  # Remove extra spaces/newlines

    return output


st.title("Anime Recommender 🎌")
st.markdown("Hey there! Tell me what your thinking, and I'll reccommend some anime based on your vibe and favorite generes")

#asks the user for their vibe
vibe= st.text_input("What is your current vibe? (eg chill, mystery, action, romcom, ect.")

#Lets the user pick one or more of their favorite generes
generes= st.multiselect(
    "Select your favorite genres:",
    #Search a anime website for some of the most popular genres
    ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life"]
)
# Display the user's vibe and selected genres
st.write(f"Your vibe: {vibe}")
st.write(f"Your favorite genres: {', '.join(generes)}")

# Button to start recommedation process
if st.button("Give me some recommendations!"):
    if vibe.strip() == "" or len(generes) == 0:
        st.error("Please enter a vibe and select at least one genre.")
    else:
        intro= generate_intro(vibe, generes)
        st.write(intro)
        st.write("Your anime recommendations are loading...")
    
        time.sleep(5)



        # Here you would call your anime recommendation function
        anime_List = query_anime(generes)
        anime_list = sorted(anime_List, key=lambda x: x['rating'], reverse=True)[:100]
        animes = recommend_anime(anime_list, vibe)

        import re

        anime_titles = []
        for line in animes.splitlines():
            line = line.strip()
            if not line:
                continue  # skip empty lines
            match = re.match(r"\d+\.\s*(.+)", line)
            if match:
                title = match.group(1).strip()
                # Remove any extra numbering at the start (e.g. "1. Planetes" or "2. 2. Planetes")
                title = re.sub(r"^\d+\.\s*", "", title)
                anime_titles.append(title)

        for title in anime_titles:
            anime = get_anime_by_title(title)
            if anime:
                st.write(f"**{anime['title']}**")
                st.image(anime['image_url'], width=200)
                st.write(f"Genres: {', '.join(anime['genres'])}")                
                st.write(f"Description: {anime['description'][:1000]}...")





    
    

    
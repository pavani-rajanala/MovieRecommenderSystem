import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Custom CSS for scaled-down pop-up effect and consistent alignment
st.markdown(
    """
    <style>
    .main {
        background-color: #1e1e1e;
        padding: 2rem;
    }
    .movie-card {
        border: none;
        border-radius: 10px;
        background: linear-gradient(to bottom, #333, #1a1a1a);
        margin: 5px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        height: 350px;  /* Ensure each card has the same height */
        width: 100%;    /* Make width consistent with column width */
        overflow: hidden;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: flex-end; /* Align text to the bottom for consistency */
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .movie-card img {
        width: 100%;
        height: 80%;
        object-fit: cover;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        color: #fff;
        text-align: center;
        padding: 10px;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
    }
    .popup {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    .popup img {
        width: 100%;
        height: auto;
        object-fit: cover;
        border-radius: 10px;
    }
    .popup .close-btn {
        display: block;
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .popup:target {
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('🍿 Movie Recommender System')
st.markdown("### Get tailored movie recommendations based on your favorites! 🎬")

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6d55c4781af5599db440d30d82ee47f0")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if 'poster_path' in data else "https://via.placeholder.com/500x750?text=No+Image+Available"

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

if st.button('Get Recommendations'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5, gap="small")
    for i, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{posters[i]}" alt="{names[i]}">
                    <div class="movie-title">{names[i]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

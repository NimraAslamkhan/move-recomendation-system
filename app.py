import streamlit as st
import pickle
import requests
import os
import streamlit.components.v1 as components

# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Load movie data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Streamlit app header
st.header("Movie Recommender System")

# Custom image carousel component
COMPONENT_DIR = os.path.join(os.getcwd(), "frontend", "public")

if not os.path.exists(COMPONENT_DIR):
    st.error(f"The component directory '{COMPONENT_DIR}' does not exist.")
else:
    imageCarouselComponent = components.declare_component("image-carousel-component", path=COMPONENT_DIR)

    # Static carousel images for demo
    imageUrls = [
        fetch_poster(1632),
        fetch_poster(299536),
        fetch_poster(17455),
        fetch_poster(2830),
        fetch_poster(429422),
        fetch_poster(9722),
        fetch_poster(13972),
        fetch_poster(240),
        fetch_poster(155),
        fetch_poster(598),
        fetch_poster(914),
        fetch_poster(255709),
        fetch_poster(572154),
    ]

    imageCarouselComponent(imageUrls=imageUrls, height=200)

# Dropdown to select a movie
selectvalue = st.selectbox("Select a movie from the dropdown:", movies_list)

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(
            list(enumerate(similarity[index])),
            reverse=True,
            key=lambda vector: vector[1]
        )
        recommend_movie = []
        recommend_poster = []
        for i in distances[1:6]:  # Top 5 recommendations
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_poster(movie_id))
        return recommend_movie, recommend_poster
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return [], []

# Button to show recommendations
if st.button("Show Recommendations"):
    if selectvalue:
        movie_name, movie_poster = recommend(selectvalue)
        if movie_name and movie_poster:
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.text(movie_name[idx])
                    st.image(movie_poster[idx])
        else:
            st.error("No recommendations found.")

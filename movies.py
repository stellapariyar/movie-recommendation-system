import pickle
import streamlit as st
from fuzzywuzzy import process  


movies = pickle.load(open('movies.pk1', 'rb'))


try:
    with open('precomputed_recommendations.pk1', 'rb') as f:
        precomputed_recommendations = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Error: 'precomputed_recommendations.pk1' not found! Please generate it first.")
    st.stop()

def get_best_match(movie_name):
    if not movie_name.strip():
        return None
    matches = process.extractOne(movie_name, movies['original_title'].values)
    return matches[0] if matches else None

def recommend(movie):
    best_match = get_best_match(movie)  # Find the closest matching movie title
    if not best_match:
        return ["No matching movie found."]

    return precomputed_recommendations.get(best_match, ["No recommendations found"])


st.title('Movie Recommender System')

selected_movie = st.selectbox("Select a movie:", movies['original_title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.write(f"### Recommended Movies for '{selected_movie}':")
    for movie in recommendations:
        st.write(f"- {movie}")

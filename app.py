import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error("Required files not found. Please make sure 'movies.pkl' and 'similarity.pkl' are available.")
    st.stop()

movies_list = movies['title'].values

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movie_posters

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Tell us your current favourite movie from below:', movies_list)

if st.button('Show Recommendation'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])

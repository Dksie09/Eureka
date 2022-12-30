import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=73abe868926a325f060798072212b7ac&language=en-US".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500"+data["poster_path"]

def fetch_overview(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=73abe868926a325f060798072212b7ac&language=en-US".format(movie_id))
    data = response.json()
    return data["overview"]

def fetch_genres(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=73abe868926a325f060798072212b7ac&language=en-US".format(movie_id))
    data = response.json()
    return data["genres"]

def recommend(movie):
    movie_index = movies[movies["title"].apply(lambda x: x.lower())==movie.lower()].index[0]
    distances = similarity[movie_index]
    similar_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in similar_movies_list:
        movie_id = movies.iloc[i[0]].id
        # st.write(movies.iloc[i[0]])
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

similarity = pickle.load(open("similarity.pkl", "rb"))
movie_list = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movie_list)

# st.markdown("WATCH<font color = 'red'>NEXT</font>!", unsafe_allow_html=True)
# st.title("WATCH*NEXT*!")
st.title("*EUREKA!*")
st.caption("Not sure what to watch next? *Let us help you!*")
select_movie = st.selectbox("What's your favourite movie?", movies["title"])

# st.sidebar.title("About")
# st.sidebar.info("This app recommends movies based on your favourite movie. It uses the cosine similarity algorithm to find similar movies. The dataset used is from Kaggle. The app is built using Streamlit and deployed on Heroku.")
if st.button("Recommend"):
    st.snow()
    cola, colb = st.columns(2)
    with cola:
        st.image(fetch_poster(movies[movies["title"].apply(lambda x: x.lower())==select_movie.lower()].id.values[0]), width=200)
    with colb:
        st.header(select_movie)
        st.write(fetch_overview(movies[movies["title"].apply(lambda x: x.lower())==select_movie.lower()].id.values[0]))
        genre_list = fetch_genres(movies[movies["title"].apply(lambda x: x.lower())==select_movie.lower()].id.values[0])
        for i in range(2):
            try:
                st.button(genre_list[i]["name"], disabled=True)
            except:
                pass
    st.subheader("You may also like:")
    try:
        names, posters = recommend(select_movie)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.write(names[0])
            st.image(posters[0])

        with col2:
            st.write(names[1])
            st.image(posters[1])

        with col3:
            st.write(names[2])
            st.image(posters[2])

        with col4:
            st.write(names[3])
            st.image(posters[3])

        with col5:
            st.write(names[4])
            st.image(posters[4])

        

    except:
        st.write("Sorry, we don't have enough data on this movie.")
    
    
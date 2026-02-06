import pickle

import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
  response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=53d1f73587897153f9c77a05378c0c38&language=en-US'.format(movie_id))
  data=response.json()
  print(data)
  return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
  
  

def recommend(movie):
  movie_index=movies[movies['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[0:6]
  recommended_movies=[]
  recommended_movies_posters=[]
  for i in movies_list:
      movie_id=movies.iloc[i[0]].id
      recommended_movies.append(movies.iloc[i[0]].title)
      recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movies_posters
  



import gzip

st.title("Movie Recommendation System")
movies_list=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_list)
similarity=pickle.load(gzip.open('similarity.pkl.gz','rb'))


selected_movie_name=st.selectbox(
  'Movie you like',
  movies['title'].values 

)

if st.button('Recommend'):
  names,posters=recommend(selected_movie_name)
  import streamlit as st

  cols = st.columns(len(names))
  for i in range(len(names)):
      with cols[i]:
          st.image(posters[i])
          st.text(names[i])

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from nltk.stem.porter import PorterStemmer
import streamlit as st

@st.cache_data
def load_data():

    df=pd.read_csv("/Users/anushatiwari/Downloads/tmdb_movies_data-2.csv")

    #Columns
    mov=df[['id','cast','director','genres','overview','original_title','keywords']]

    mov=mov.dropna()

    def std_form(obj):
        return obj.replace("|", " ").split()

    mov.loc[:,'genres']=mov['genres'].apply(std_form)
    mov.loc[:,'keywords']=mov['keywords'].apply(std_form)
    mov.loc[:,'cast']=mov['cast'].apply(std_form)
    mov.loc[:,'director']=mov['director'].apply(std_form)
    mov.loc[:,'overview']=mov['overview'].apply(lambda i: i.split())


    ps=PorterStemmer()
    def stem(text):
        return " ".join([ps.stem(word) for word in text.split()])

    mov['gen_stem'] = mov['genres'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
    mov['key_stem'] = mov['keywords'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
    mov['over_stem'] = mov['overview'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
    mov['cast_stem'] = mov['cast'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
    mov['dir_stem'] = mov['director'].apply(lambda i: " ".join([ps.stem(e) for e in i]))

    mov['tags'] = (mov['cast_stem'] + " " + mov['gen_stem'] + " " +
    mov['dir_stem'] + " " + mov['over_stem'] + " " + mov['key_stem'])

    df2 = mov[['id', 'original_title', 'tags']].copy()
    df2['tags'] = df2['tags'].apply(lambda x: " ".join(x.split()))
    df2['tags'] = df2['tags'].apply(lambda x: " ".join([ps.stem(word) for word in x.split()]))
    
    cnt_vec=cv(max_features=10000, stop_words = 'english')
    vec=cnt_vec.fit_transform(df2['tags']).toarray()

    sim=cosine_similarity(vec)

    pickle.dump(df2,open('mov.pkl','wb'))
    pickle.dump(df2.to_dict(),open('mov_dict.pkl','wb'))
    pickle.dump(sim,open('sim.pkl','wb'))
    
    return df2,sim,mov

df2, sim,mov = load_data()

def recom(movie):
    ind=df2[df2['original_title']==movie].index[0]
    dist=sim[ind]
    mov_lst=sorted(list(enumerate(dist)),reverse=True,key=lambda y: y[1])[1:6]

    rec_mov=[]
    rec_gen=[]

    for i in mov_lst:
        rec_mov.append(mov.iloc[i[0]].original_title)
        rec_gen.append(mov.iloc[i[0]].genres)
    
    return rec_mov,rec_gen

#loading
mov_dict=pickle.load(open('mov_dict.pkl','rb'))
df2=pd.DataFrame(mov_dict)
sim=pickle.load(open('sim.pkl','rb'))

st.markdown("<h1 style='color: white; font-weight: bold;'>Movie Recommender System</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: white; margin-bottom: 0;'>Select a movie to recommend</p>", unsafe_allow_html=True)
sel_movie_name = st.selectbox(
    '',
    df2['original_title'].values)


if st.button('Recommend'):
    names, genres = recom(sel_movie_name)

    for name, genre in zip(names, genres):
        
        st.markdown(f'<div style="background-color:#808080; border-radius:5px;">{name} - {genre}</div>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bW92aWV8ZW58MHx8MHx8fDA%3D");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

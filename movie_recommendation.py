import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from nltk.stem.porter import PorterStemmer
import streamlit as st

df=pd.read_csv("/Users/anushatiwari/Downloads/tmdb_movies_data-2.csv")

#Columns
mov=df[['id','cast','director','genres','overview','original_title','keywords']]

mov=mov.dropna()

def std_form(obj):
    s=list(obj)
    for a in range(len(s)):
        if s[a]=='|':
            s[a]==" "
    temp = "".join(s)
    temp_lst=temp.split()
    return temp_lst

mov.loc[:,'genres']=mov['genres'].apply(convert)
mov.loc[:,'keywords']=mov['keywords'].apply(convert)
mov.loc[:,'cast']=mov['cast'].apply(convert)
mov.loc[:,'director']=mov['director'].apply(convert)
mov.loc[:,'overview']=mov['overview'].apply(lambda i: i.split())

ps=PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

mov.loc[:,'genres']=mov['genres'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
mov.loc[:,'keywords']=mov['keywords'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
mov.loc[:,'overview']=mov['overview'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
mov.loc[:,'cast']=mov['cast'].apply(lambda i: " ".join([ps.stem(e) for e in i]))
mov.loc[:,'director']=mov['director'].apply(lambda i: " ".join([ps.stem(e) for e in i]))

mov.loc[:, 'tags'] = mov['cast']+mov['genres']+mov['director'] + mov['overview'] + mov['keywords']

df2=mov[['id','original_title','tags']].copy()
df2.loc[:,'tags']=df2['tags'].apply(lambda x: " ".join(x.split()))
df2.loc[:,'tags']=df2['tags'].apply(stem)

cnt_vec=cv(max_faetures=10000, stop_words = 'english')
vec=cnt_vec.fit_transform(df2['tags']).toarray()

sim=cosine_similarity(vec)

pickle.dump(df2,open('mov.pkl','wb'))
pickle.dump(df2.to_dict(),open('mov_dict.pkl','wb'))
pickle.dump(sim,open('sim.pkl','wb'))

def recom(movie):
    ind=df2[df2['original_title']==movie].index[0]
    dist=sim[ind]
    mov_lst=sorted(list(ennumerate(dist)),reverse=True,key=lambda y: y[1])[1:6]

    rec_mov=[]
    rec_gen=[]

    for i mov_lst:
        rec_mov.append(mov.iloc[i[0]].original_title)
        rec_gen.append(mov.iloc[i[0]].genres)
    
    return rec_mov,rec_gen

#loading
mov_dict=pickle.load(open('mov_dict.pkl','rb'))
df2=pd.Dataframe(mov_dict)
sim=pickle.load(open('sim.pkl','rb'))

st.title("Movie Recommendation System")
st.markdown("""
<style>
.stApp{
    background-image: url("https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bW92aWV8ZW58MHx8MHx8fDA%3D");
    background-size: cover;
}
</style>
""",
unsafe_allow_html=True)

sel_mov=st.selectbox('Select a movie so that we recommend you more like it',df2['original_title'].values)

if st.button('Recommend'):
    n1,g1 = recom(sel_mov)
    for n,g in zip(n1,g1):
        st.write("Movie name: {n} Genre: {g}")



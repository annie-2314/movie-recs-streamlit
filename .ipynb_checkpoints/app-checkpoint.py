import streamlit as st
import pickle
import pandas as pd
import requests

df = pickle.load(open("movies.pkl", "rb"))
df = pd.DataFrame(df)
cs = pickle.load(open("cs.pkl", "rb"))


def fetch_poster(MOVIE_ID):
    API_KEY = "6582af9236100db9aa52fa072a1ed070"
    url = f'https://api.themoviedb.org/3/movie/{MOVIE_ID}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None


def recommend(movie):
    idx = df[df["title"] == movie].index[0]
    dist = cs[idx]
    similar5 = sorted(list(enumerate(dist)),
                      key=lambda x: x[1], reverse=True)[1:6]
    m_list = []
    for i, cos_sim in similar5:
        m_list.append((df.iloc[i]["id"], df.iloc[i]["title"]))
    return m_list


st.title("Get new recommendations based on your favourite movies!")

sel_movie = st.selectbox("Choose a movie:", df["title"].values)

if st.button("Show recommendations"):
    rcm = recommend(sel_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            poster_url = fetch_poster(rcm[i][0])
            if poster_url:
                st.image(poster_url, caption=rcm[i][1], use_column_width=True)
            else:
                st.write("No poster available for " + rcm[i][1])

centered_footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: grey;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
.footer a {
    color: #0e1117;
    text-decoration: none;
}
</style>
<div class="footer">
    <p>Project by: Annie Siri</p>
</div>
"""
st.markdown(centered_footer, unsafe_allow_html=True)

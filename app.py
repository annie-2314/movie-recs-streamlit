import streamlit as st
import pickle
import pandas as pd
import requests
import base64

df = pickle.load(open("movies.pkl", "rb"))
df = pd.DataFrame(df)
cs = pickle.load(open("cs.pkl", "rb"))

# Function to fetch movie poster
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

# Function to recommend similar movies
def recommend(movie):
    idx = df[df["title"] == movie].index[0]
    dist = cs[idx]
    similar5 = sorted(list(enumerate(dist)),
                      key=lambda x: x[1], reverse=True)[1:6]
    m_list = []
    for i, cos_sim in similar5:
        m_list.append((df.iloc[i]["id"], df.iloc[i]["title"]))
    return m_list

# Title
st.markdown("<h1 style='color:white;'>🎥 TMDb Movie Recommendation Engine</h1>", unsafe_allow_html=True)

# Movie selection
sel_movie = st.selectbox("Choose a movie:", df["title"].values)

# Display recommendations on button click
if st.button("Show recommendations"):
    rcm = recommend(sel_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            poster_url = fetch_poster(rcm[i][0])
            if poster_url:
                st.image(poster_url, caption=rcm[i][1], use_container_width=True)  # Update here
                
            else:
                st.write("No poster available for " + rcm[i][1])

# Footer
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
    color: black;
    text-decoration: none;
}
</style>
<div class="footer">
    <p>Project by: Annie Siri</p>
</div>
"""
st.markdown(centered_footer, unsafe_allow_html=True)

# Function to encode local image to base64 (Optional: only if you want to use base64 method)
def get_base64_bg(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set a background image using CSS (choose one method, here we are using base64 encoding)
bg_base64 = get_base64_bg("bg.png")  # Adjust path if necessary

# CSS with base64-encoded image
bg_css = f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

# Apply the CSS for the background image
st.markdown(bg_css, unsafe_allow_html=True)

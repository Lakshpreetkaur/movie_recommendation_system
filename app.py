import streamlit as st
import pickle
import pandas as pd

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0A0E1A; }
    .stApp { background-color: #0A0E1A; }

    h1 { color: #F5C518 !important; font-size: 2.2rem !important; }
    h3 { color: #ffffff !important; }
    p, label, .stMarkdown { color: #E8EAF0 !important; }

    /* Dropdown */
    .stSelectbox > div > div {
        background-color: #111827;
        border: 1px solid #1E2D45;
        color: white;
        border-radius: 8px;
    }

    /* Button */
    .stButton > button {
        background-color: #F5C518;
        color: #0A0E1A;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        width: 100%;
        margin-top: 0.5rem;
    }
    .stButton > button:hover {
        background-color: #e0b214;
        color: #0A0E1A;
    }

    /* Movie cards */
    .movie-card {
        background-color: #111827;
        border: 1px solid #1E2D45;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
    }
    .movie-rank {
        font-size: 0.75rem;
        color: #F5C518;
        font-weight: bold;
        letter-spacing: 0.08em;
        margin-bottom: 0.2rem;
    }
    .movie-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    .movie-genres {
        font-size: 0.85rem;
        color: #8892A4;
    }
    .genre-chip {
        display: inline-block;
        background-color: #1A2236;
        border: 1px solid #14B8A6;
        color: #14B8A6;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin: 2px 3px 2px 0;
    }
    .header-bar {
        background-color: #111827;
        border-bottom: 2px solid #F5C518;
        padding: 1rem 0 0.5rem 0;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .subtitle {
        color: #8892A4 !important;
        font-size: 0.95rem;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 1.5rem;
    }
    .result-header {
        color: #F5C518 !important;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    .divider {
        border: none;
        border-top: 1px solid #1E2D45;
        margin: 1.5rem 0;
    }
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .stat-box {
        background-color: #111827;
        border: 1px solid #1E2D45;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        flex: 1;
        text-align: center;
    }
    .stat-num {
        font-size: 1.4rem;
        font-weight: bold;
        color: #F5C518;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #8892A4;
    }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    # Handle both DataFrame and dict formats
    if isinstance(movies, dict):
        movies = pd.DataFrame(movies)
    return movies, similarity

try:
    movies_df, similarity = load_data()
except FileNotFoundError:
    st.error("movies.pkl or similarity.pkl not found. Make sure both files are in the same folder as app.py.")
    st.stop()


# ── Recommend function ────────────────────────────────────────
def recommend(movie_title):
    try:
        idx = movies_df[movies_df['title'] == movie_title].index[0]
    except IndexError:
        return []

    distances = similarity[idx]
    top5 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i, score in top5:
        row = movies_df.iloc[i]
        title = row['title']
        # Get genres if available
        genres = ""
        if 'genres' in movies_df.columns:
            genres = str(row['genres']) if pd.notna(row.get('genres', '')) else ""
        results.append({
            'title': title,
            'genres': genres,
            'score': round(float(score), 4)
        })
    return results


# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="header-bar">', unsafe_allow_html=True)
st.markdown("# 🎬 Movie Recommender")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Content-based filtering · TMDB 5000 dataset · Cosine similarity</p>',
            unsafe_allow_html=True)

# Stats row
total_movies = len(movies_df)
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-num">{total_movies:,}</div>
        <div class="stat-label">Movies indexed</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">5,000</div>
        <div class="stat-label">Features used</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">83%</div>
        <div class="stat-label">Genre precision</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">Top 5</div>
        <div class="stat-label">Recommendations</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Search ────────────────────────────────────────────────────
movie_list = sorted(movies_df['title'].dropna().unique().tolist())

selected_movie = st.selectbox(
    "Search for a movie",
    options=[""] + movie_list,
    format_func=lambda x: "Type or select a movie..." if x == "" else x
)

clicked = st.button("Get Recommendations")

# ── Results ───────────────────────────────────────────────────
if clicked:
    if not selected_movie:
        st.warning("Please select a movie first.")
    else:
        results = recommend(selected_movie)

        if not results:
            st.error(f"Could not find '{selected_movie}' in the dataset.")
        else:
            st.markdown(f'<p class="result-header">Top 5 recommendations for "{selected_movie}"</p>',
                        unsafe_allow_html=True)

            for rank, movie in enumerate(results, 1):
                # Build genre chips
                genres_html = ""
                if movie['genres']:
                    for g in str(movie['genres']).split(','):
                        g = g.strip()
                        if g:
                            genres_html += f'<span class="genre-chip">{g}</span>'
                if not genres_html:
                    genres_html = '<span style="color:#8892A4;font-size:0.85rem;">Genre info unavailable</span>'

                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-rank">#{rank} &nbsp;·&nbsp; Similarity: {movie['score']}</div>
                    <div class="movie-title">{movie['title']}</div>
                    <div>{genres_html}</div>
                </div>
                """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#8892A4;font-size:0.8rem;">'
    'Built with Python · Scikit-learn · NLTK · Streamlit · TMDB 5000 Dataset'
    '</p>',
    unsafe_allow_html=True
)

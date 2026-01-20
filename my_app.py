# # -*- coding: utf-8 -*-
# """
# ================================================================================
# STREAMLENS - NETFLIX-STYLE MOVIE RECOMMENDATION SYSTEM
# ================================================================================

# Modern Netflix-inspired UI with Real Movie Posters

# Features:
# ---------
# 1. Real movie posters from TMDb API
# 2. User-based recommendations
# 3. Movie search with similar movies
# 4. Business insights dashboard
# 5. Visual movie browsing

# Author: NLC
# Date: December 2025
# ================================================================================
# """

# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import os
# import requests
# from datetime import datetime
# import plotly.express as px
# import plotly.graph_objects as go

# # Page configuration
# st.set_page_config(
#     page_title="StreamFlix",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for Netflix-style interface
# st.markdown("""
# <style>
#     /* Global styles */
#    /* App background */
# .stApp {
#     background: linear-gradient(135deg, #1a0033 0%, #0a0015 50%, #1a1a3e 100%);
#     color: #ffffff;
# }
    
#     .stApp {
#         background-color: #141414;
#     }
    
#     /* Hide default Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
    
#     /* Header styles */
#     .header-container {
#         background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
#         padding: 20px 40px;
#         margin-bottom: 20px;
#     }
    
#     .logo {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #e50914;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
#         margin-bottom: 20px;
#     }
    
#     .nav-menu {
#         display: flex;
#         gap: 20px;
#         margin: 20px 0;
#     }
    
#     .nav-item {
#         color: #e5e5e5;
#         font-size: 1rem;
#         padding: 5px 10px;
#         cursor: pointer;
#         transition: color 0.3s;
#     }
    
#     .nav-item:hover {
#         color: #b3b3b3;
#     }
    
#     /* Section styles */
#     .section-title {
#         font-size: 1.8rem;
#         font-weight: bold;
#         color: #e5e5e5;
#         margin: 40px 0 20px 40px;
#     }
    
#     /* Movie grid */
#     .movie-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
#         gap: 15px;
#         padding: 0 40px;
#         margin-bottom: 40px;
#     }
    
#     .movie-card {
#         position: relative;
#         border-radius: 8px;
#         overflow: hidden;
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#         cursor: pointer;
#         background: #2f2f2f;
#         aspect-ratio: 2/3;
#     }
    
#     .movie-card:hover {
#         transform: scale(1.05);
#         z-index: 10;
#         box-shadow: 0 8px 16px rgba(0,0,0,0.6);
#     }
    
#     .movie-poster {
#         width: 100%;
#         height: 100%;
#         object-fit: cover;
#     }
    
#     .movie-overlay {
#         position: absolute;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background: linear-gradient(transparent, rgba(0,0,0,0.95));
#         padding: 40px 10px 10px 10px;
#     }
    
#     .movie-title {
#         font-size: 0.9rem;
#         font-weight: bold;
#         margin-bottom: 4px;
#     }
    
#     .movie-year {
#         font-size: 0.75rem;
#         color: #999;
#     }
    
#     .movie-rating {
#         position: absolute;
#         top: 10px;
#         right: 10px;
#         background: rgba(0,0,0,0.8);
#         padding: 4px 8px;
#         border-radius: 4px;
#         font-size: 0.8rem;
#         font-weight: bold;
#         color: #ffd700;
#     }
    
#     /* User selection panel */
#     .selection-panel {
#         background: #1f1f1f;
#         padding: 30px;
#         border-radius: 10px;
#         margin: 20px 40px;
#     }
    
#     /* Insight cards */
#     .insight-card {
#         background: #1f1f1f;
#         padding: 20px;
#         border-radius: 10px;
#         margin: 10px 0;
#     }
    
#     .metric-value {
#         font-size: 2rem;
#         font-weight: bold;
#         color: #e50914;
#     }
    
#     .metric-label {
#         font-size: 1rem;
#         color: #999;
#     }
    
#     /* Responsive */
#     @media (max-width: 768px) {
#         .movie-grid {
#             grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
#             gap: 10px;
#             padding: 0 20px;
#         }
#         .section-title {
#             margin-left: 20px;
#         }
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================================================
# # TMDB API INTEGRATION
# # ============================================================================

# TMDB_API_KEY = "0503920ea26bcfe7e9d75fa205d2513f"  # Replace with your TMDb API key
# TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# @st.cache_data(ttl=3600)
# def get_movie_poster(title, year=None):
#     """Fetch high-quality movie poster from TMDb"""
#     try:
#         # Clean MovieLens-style titles
#         clean_title = title.split('(')[0].strip()

#         # Handle "Godfather, The" → "The Godfather"
#         if ',' in clean_title:
#             parts = clean_title.split(',')
#             if parts[-1].strip().lower() in ['the', 'a', 'an']:
#                 clean_title = f"{parts[-1].strip()} {parts[0].strip()}"

#         search_url = "https://api.themoviedb.org/3/search/movie"
#         params = {
#             "api_key": TMDB_API_KEY,
#             "query": clean_title,
#             "include_adult": False
#         }

#         if year:
#             params["year"] = int(year)

#         r = requests.get(search_url, params=params, timeout=6)
#         r.raise_for_status()
#         data = r.json()

#         if data["results"]:
#             poster_path = data["results"][0].get("poster_path")
#             if poster_path:
#                 return f"https://image.tmdb.org/t/p/w500{poster_path}"

#     except Exception as e:
#         pass

#     # Fallback Netflix-style placeholder
#     return "https://via.placeholder.com/500x750/141414/E50914?text=No+Poster"

# # ============================================================================
# # DATA & MODEL LOADING
# # ============================================================================

# @st.cache_data
# def load_data(base_path):
#     """Load processed data"""
#     try:
#         movies = pd.read_csv(os.path.join(base_path, 'movies_processed.csv'))
#         ratings = pd.read_csv(os.path.join(base_path, 'ratings_processed.csv'))
#         user_stats = pd.read_csv(os.path.join(base_path, 'user_statistics.csv'))
#         genre_stats = pd.read_csv(os.path.join(base_path, 'genre_statistics.csv'))
#         return movies, ratings, user_stats, genre_stats
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         # Create sample data
#         movies = pd.DataFrame({
#             'movieId': range(1, 101),
#             'title': [f'Movie {i} (1995)' for i in range(1, 101)],
#             'genres': ['Action|Adventure'] * 100
#         })
#         ratings = pd.DataFrame({
#             'userId': [1] * 100,
#             'movieId': range(1, 101),
#             'rating': np.random.uniform(3, 5, 100),
#             'timestamp': [datetime.now()] * 100
#         })
#         user_stats = pd.DataFrame()
#         genre_stats = pd.DataFrame()
#         return movies, ratings, user_stats, genre_stats

# @st.cache_resource
# def load_models(models_path):
#     """Load trained models"""
#     try:
#         baseline = joblib.load(os.path.join(models_path, 'baseline_popularity.pkl'))
#         best_model = joblib.load(os.path.join(models_path, 'lasso.pkl'))
#         return baseline, best_model
#     except:
#         return None, None

# # Set paths
# BASE_PATH = "C:/Users/User/Downloads/ml-latest/ml-latest/output"
# MODELS_PATH = os.path.join(BASE_PATH, 'models')
# PLOTS_PATH = os.path.join(BASE_PATH, 'plots')

# # Load data
# movies, ratings, user_stats, genre_stats = load_data(BASE_PATH)
# baseline_model, best_model = load_models(MODELS_PATH)

# # Extract year from title
# def extract_year(title):
#     """Extract year from movie title"""
#     import re
#     match = re.search(r'\((\d{4})\)', str(title))
#     return match.group(1) if match else None

# movies['year'] = movies['title'].apply(extract_year)
# movies['clean_title'] = movies['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)

# # Calculate movie scores if not in baseline model
# if baseline_model is None:
#     movie_stats = ratings.groupby('movieId').agg({
#         'rating': ['mean', 'count']
#     }).reset_index()
#     movie_stats.columns = ['movieId', 'avg_rating', 'vote_count']
    
#     C = movie_stats['avg_rating'].mean()
#     m = movie_stats['vote_count'].quantile(0.7)
#     movie_stats['weighted_score'] = (
#         (movie_stats['vote_count'] / (movie_stats['vote_count'] + m)) * movie_stats['avg_rating'] +
#         (m / (movie_stats['vote_count'] + m)) * C
#     )
    
#     movies = movies.merge(movie_stats, on='movieId', how='left')
# else:
#     movies = movies.merge(
#         baseline_model['movie_scores'][['movieId', 'avg_rating', 'vote_count', 'weighted_score']],
#         on='movieId',
#         how='left'
#     )

# movies['avg_rating'] = movies['avg_rating'].fillna(3.0)
# movies['weighted_score'] = movies['weighted_score'].fillna(3.0)

# # ============================================================================
# # SESSION STATE
# # ============================================================================

# if 'page' not in st.session_state:
#     st.session_state.page = 'home'
# if 'selected_movie' not in st.session_state:
#     st.session_state.selected_movie = None

# # ============================================================================
# # MOVIE DISPLAY FUNCTION
# # ============================================================================

# def display_movie_grid(movie_list, title="Movies", show_search=False, section_id="default"):
#     """Display movies in a grid layout with real posters"""
#     st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    
#     # Create grid with columns
#     cols_per_row = 6
#     rows = [movie_list.iloc[i:i + cols_per_row] for i in range(0, len(movie_list), cols_per_row)]
    
#     for row in rows:
#         cols = st.columns(cols_per_row)
#         for idx, (_, movie) in enumerate(row.iterrows()):
#             with cols[idx]:
#                 # Get poster URL
#                 poster_url = get_movie_poster(movie['title'], movie['year'])
                
#                 # Create clickable movie card
#                 rating_display = f"{movie['avg_rating']:.1f}⭐" if pd.notna(movie['avg_rating']) else "N/A"
                
#                 # Display poster image
#                 st.image(poster_url, use_container_width=True)
                
#                 # Movie info overlay
#                 st.markdown(f"""
#                 <div style='margin-top: -60px; position: relative; z-index: 1;'>
#                     <div class="movie-overlay">
#                         <div class="movie-title">{movie['clean_title'][:30]}{'...' if len(movie['clean_title']) > 30 else ''}</div>
#                         <div class="movie-year">{movie['year'] if movie['year'] else 'N/A'} • {rating_display}</div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 # Add click handler for similar movies
#                 if show_search and st.button(
#                     "Similar",
#                     key=f"sim_{section_id}_{movie['movieId']}",
#                     use_container_width=True
#                 ):
#                     st.session_state.selected_movie = movie['movieId']
#                     st.session_state.page = 'similar'
#                     st.rerun()


# # ============================================================================
# # HEADER & NAVIGATION
# # ============================================================================

# st.markdown('<div class="header-container">', unsafe_allow_html=True)

# # Logo and Search
# col1, col2 = st.columns([1, 3])
# with col1:
#     st.markdown('<div class="logo">StreamLens</div>', unsafe_allow_html=True)

# with col2:
#     search_col, button_col = st.columns([5, 1])
#     with search_col:
#         search_query = st.text_input(
#             "Search",
#             placeholder="Search movies...",
#             label_visibility="collapsed",
#             key="search"
#         )
#     with button_col:
#         search_button = st.button("Search", type="primary")

# # Navigation
# nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
# with nav_col1:
#     if st.button("🏠 Home", use_container_width=True):
#         st.session_state.page = 'home'
#         st.rerun()
# with nav_col2:
#     if st.button("👤 Recommendations", use_container_width=True):
#         st.session_state.page = 'recommendations'
#         st.rerun()
# with nav_col3:
#     if st.button("🔍 Search Movies", use_container_width=True):
#         st.session_state.page = 'search'
#         st.rerun()
# with nav_col4:
#     if st.button("📊 Insights", use_container_width=True):
#         st.session_state.page = 'insights'
#         st.rerun()

# st.markdown('</div>', unsafe_allow_html=True)

# # ============================================================================
# # MAIN CONTENT BASED ON PAGE
# # ============================================================================

# # Handle search from header
# if search_query and search_button:
#     st.session_state.page = 'search_results'
#     st.session_state.search_query = search_query

# # HOME PAGE
# if st.session_state.page == 'home':
#     # Trending Now
#     trending_movies = movies.sort_values('weighted_score', ascending=False).head(18)
#     display_movie_grid(trending_movies, "Trending ", True, "home_trending")
    
#     # Top Rated
#     top_rated = movies.sort_values('avg_rating', ascending=False).head(18)
#     display_movie_grid(top_rated, "⭐ Top Rated", show_search=True)
    
#     # Popular by Genre
#     if 'genres' in movies.columns:
#         for genre in ['Action', 'Comedy', 'Drama', 'Thriller', 'Romance']:
#             genre_movies = movies[
#                 movies['genres'].str.contains(genre, na=False)
#             ].sort_values('weighted_score', ascending=False).head(12)
            
#             if len(genre_movies) > 0:
#                 display_movie_grid(
#     genre_movies,
#     f"🎬 {genre} Movies",
#     True,
#     f"home_genre_{genre}"
# )
# # USER RECOMMENDATIONS PAGE
# elif st.session_state.page == 'recommendations':
#     st.markdown('<div class="section-title">👤 Personalized Recommendations</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns([2, 1, 1])
    
#     with col1:
#         user_id = st.selectbox(
#             "Select User ID",
#             options=sorted(ratings['userId'].unique()[:500]),
#             help="Choose a user to see personalized recommendations"
#         )
    
#     with col2:
#         n_recommendations = st.slider(
#             "Number of Movies",
#             min_value=6,
#             max_value=36,
#             value=18,
#             step=6
#         )
    
#     with col3:
#         genres_list = ['All Genres'] + sorted(
#             set(g for sublist in movies['genres'].str.split('|').dropna()
#             for g in sublist if g != '(no genres listed)')
#         )
#         genre_filter = st.selectbox("Genre Filter", genres_list)
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     if user_id:
#         # Get user's watched movies
#         user_ratings = ratings[ratings['userId'] == user_id]
#         watched_movies = set(user_ratings['movieId'])
        
#         # Get recommendations
#         recommendations = movies[~movies['movieId'].isin(watched_movies)].copy()
        
#         # Apply genre filter
#         if genre_filter != 'All Genres':
#             recommendations = recommendations[
#                 recommendations['genres'].str.contains(genre_filter, na=False)
#             ]
        
#         recommendations = recommendations.sort_values('weighted_score', ascending=False).head(n_recommendations)
        
#         # User profile
#         st.markdown('<div class="section-title">📊 User Profile</div>', unsafe_allow_html=True)
        
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.markdown(f'<div class="insight-card"><div class="metric-value">{len(user_ratings)}</div><div class="metric-label">Movies Rated</div></div>', unsafe_allow_html=True)
#         with col2:
#             st.markdown(f'<div class="insight-card"><div class="metric-value">{user_ratings["rating"].mean():.2f}⭐</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)
#         with col3:
#             top_genre = user_ratings.merge(movies, on='movieId')['genres'].str.split('|').explode().mode()
#             top_genre_str = top_genre[0] if len(top_genre) > 0 else 'N/A'
#             st.markdown(f'<div class="insight-card"><div class="metric-value">{top_genre_str[:15]}</div><div class="metric-label">Favorite Genre</div></div>', unsafe_allow_html=True)
#         with col4:
#             rating_bias = "Generous" if user_ratings['rating'].mean() > 3.5 else "Critical"
#             st.markdown(f'<div class="insight-card"><div class="metric-value">{rating_bias}</div><div class="metric-label">Rating Style</div></div>', unsafe_allow_html=True)
        
#         # Display recommendations
#         display_movie_grid(recommendations, f"🎯 Recommended for User {user_id}")

# # SEARCH MOVIES PAGE
# elif st.session_state.page == 'search' or st.session_state.page == 'search_results':
#     st.markdown('<div class="section-title">🔍 Search & Discover</div>', unsafe_allow_html=True)
    
#     if st.session_state.page == 'search_results' and 'search_query' in st.session_state:
#         query = st.session_state.search_query
#     else:
#         st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
#         query = st.text_input("Search for movies", placeholder="Enter movie title...")
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     if query:
#         search_results = movies[
#             movies['title'].str.contains(query, case=False, na=False)
#         ].sort_values('weighted_score', ascending=False).head(24)
        
#         if len(search_results) > 0:
#             display_movie_grid(search_results, f"Search Results: '{query}'", show_search=True)
#         else:
#             st.warning("No movies found. Try a different search term.")

# # SIMILAR MOVIES PAGE
# elif st.session_state.page == 'similar':
#     if st.session_state.selected_movie:
#         selected = movies[movies['movieId'] == st.session_state.selected_movie].iloc[0]
        
#         st.markdown(f'<div class="section-title">🎬 Similar to: {selected["title"]}</div>', unsafe_allow_html=True)
        
#         # Find similar movies based on genres
#         movie_genres = set(selected['genres'].split('|'))
        
#         similar_movies = movies[movies['movieId'] != st.session_state.selected_movie].copy()
#         similar_movies['similarity'] = similar_movies['genres'].apply(
#             lambda x: len(set(x.split('|')) & movie_genres) / len(movie_genres) if pd.notna(x) else 0
#         )
        
#         similar_movies = similar_movies[similar_movies['similarity'] > 0].sort_values(
#             ['similarity', 'weighted_score'], ascending=[False, False]
#         ).head(24)
        
#         display_movie_grid(similar_movies, "🎯 Movies You Might Like", show_search=True)

# # INSIGHTS PAGE
# elif st.session_state.page == 'insights':
#     st.markdown('<div class="section-title">📊 Business Insights Dashboard</div>', unsafe_allow_html=True)
    
#     # Key Metrics
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.markdown(f'<div class="insight-card"><div class="metric-value">{len(movies):,}</div><div class="metric-label">Total Movies</div></div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown(f'<div class="insight-card"><div class="metric-value">{len(ratings):,}</div><div class="metric-label">Total Ratings</div></div>', unsafe_allow_html=True)
#     with col3:
#         st.markdown(f'<div class="insight-card"><div class="metric-value">{ratings["userId"].nunique():,}</div><div class="metric-label">Active Users</div></div>', unsafe_allow_html=True)
#     with col4:
#         st.markdown(f'<div class="insight-card"><div class="metric-value">{ratings["rating"].mean():.2f}⭐</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Genre Performance
#     if genre_stats is not None and not genre_stats.empty:
#         st.markdown('<div class="section-title">🎭 Genre Performance</div>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             fig1 = px.bar(
#                 genre_stats.sort_values('avg_rating', ascending=False).head(10),
#                 x='avg_rating',
#                 y='genre',
#                 orientation='h',
#                 title='Top 10 Genres by Rating',
#                 color='avg_rating',
#                 color_continuous_scale='RdYlGn',
#                 template='plotly_dark'
#             )
#             fig1.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f')
#             st.plotly_chart(fig1, use_container_width=True)
        
#         with col2:
#             fig2 = px.bar(
#                 genre_stats.sort_values('n_ratings', ascending=False).head(10),
#                 x='n_ratings',
#                 y='genre',
#                 orientation='h',
#                 title='Top 10 Most Popular Genres',
#                 color='n_ratings',
#                 color_continuous_scale='Blues',
#                 template='plotly_dark'
#             )
#             fig2.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f')
#             st.plotly_chart(fig2, use_container_width=True)
    
#     # Rating Distribution
#     st.markdown('<div class="section-title">📈 Rating Distribution</div>', unsafe_allow_html=True)
    
#     fig3 = px.histogram(
#         ratings,
#         x='rating',
#         nbins=10,
#         title='Distribution of Ratings',
#         color_discrete_sequence=['#e50914'],
#         template='plotly_dark'
#     )
#     fig3.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f')
#     st.plotly_chart(fig3, use_container_width=True)

# # ============================================================================
# # FOOTER
# # ============================================================================

# st.markdown("<br><br>", unsafe_allow_html=True)
# st.markdown("""
# <div style='text-align: center; color: #666; padding: 40px;'>
#     <p style='font-size: 0.9rem;'>StreamRec - Powered by MovieLens & TMDb</p>
#     <p style='font-size: 0.8rem;'>ML Recommendation System • December 2025</p>
# </div>
# """, unsafe_allow_html=True)


# -*- coding: utf-8 -*-
"""
================================================================================
STREAMLENS - NETFLIX-STYLE MOVIE RECOMMENDATION SYSTEM
================================================================================

Modern Netflix-inspired UI with Real Movie Posters

Features:
---------
1. Real movie posters from TMDb API
2. User-based recommendations
3. Movie search with similar movies
4. Business insights dashboard
5. Visual movie browsing

Author: NLC
Date: December 2025
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import re

# Page configuration
st.set_page_config(
    page_title="StreamFlix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- Custom CSS --------------------
st.markdown("""<style>
.stApp {background: linear-gradient(135deg, #1a0033 0%, #0a0015 50%, #1a1a3e 100%); color: #ffffff;}
#MainMenu {visibility: hidden;} footer {visibility: hidden;}
.header-container {background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%); padding: 20px 40px; margin-bottom: 20px;}
.logo {font-size: 2.5rem; font-weight: bold; color: #e50914; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin-bottom: 20px;}
.nav-menu {display: flex; gap: 20px; margin: 20px 0;}
.nav-item {color: #e5e5e5; font-size: 1rem; padding: 5px 10px; cursor: pointer; transition: color 0.3s;}
.nav-item:hover {color: #b3b3b3;}
.section-title {font-size: 1.8rem; font-weight: bold; color: #e5e5e5; margin: 40px 0 20px 40px;}
.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 15px;
    padding: 0 40px;
    margin-bottom: 40px;
}

/* 🔒 FIXED CARD SIZE */
.movie-card {
    position: relative;
    width: 100%;
    height: 270px;                 /* FIXED HEIGHT */
    border-radius: 8px;
    overflow: hidden;
    background: #2f2f2f;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover {
    transform: scale(1.05);
    z-index: 10;
    box-shadow: 0 8px 16px rgba(0,0,0,0.6);
}

/* 🔒 FIXED POSTER CONTAINER */
.poster-container {
    width: 100%;
    height: 100%;
    position: relative;
}

/* 🔒 FORCE IMAGE TO FILL SPACE */
.poster-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Overlay */
.movie-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.95));
    padding: 40px 10px 10px 10px;
}

.movie-title {
    font-size: 0.9rem;
    font-weight: bold;
    margin-bottom: 4px;
}

.movie-year {
    font-size: 0.75rem;
    color: #999;
.movie-rating {position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: #ffd700;}
.selection-panel {background: #1f1f1f; padding: 30px; border-radius: 10px; margin: 20px 40px;}
.insight-card {background: #1f1f1f; padding: 20px; border-radius: 10px; margin: 10px 0;}
.metric-value {font-size: 2rem; font-weight: bold; color: #e50914;}
.metric-label {font-size: 1rem; color: #999;}
@media (max-width: 768px) {
    .movie-grid {grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; padding: 0 20px;}
    .section-title {margin-left: 20px;}
}
</style>""", unsafe_allow_html=True)

# -------------------- TMDB API --------------------
TMDB_API_KEY = "0503920ea26bcfe7e9d75fa205d2513f"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

@st.cache_data(ttl=3600)
def get_movie_poster(title, year=None):
    try:
        clean_title = title.split('(')[0].strip()
        if ',' in clean_title:
            parts = clean_title.split(',')
            if parts[-1].strip().lower() in ['the', 'a', 'an']:
                clean_title = f"{parts[-1].strip()} {parts[0].strip()}"
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": clean_title, "include_adult": False}
        if year: params["year"] = int(year)
        r = requests.get(search_url, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path: return f"{TMDB_IMAGE_BASE}{poster_path}"
    except: pass
    return "https://via.placeholder.com/500x750/141414/E50914?text=No+Poster"

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data(base_path):
    try:
        movies = pd.read_csv(os.path.join(base_path, 'movies_processed.csv'))
        ratings = pd.read_csv(os.path.join(base_path, 'ratings_processed.csv'))
        user_stats = pd.read_csv(os.path.join(base_path, 'user_statistics.csv'))
        genre_stats = pd.read_csv(os.path.join(base_path, 'genre_statistics.csv'))
        return movies, ratings, user_stats, genre_stats
    except:
        movies = pd.DataFrame({
            'movieId': range(1, 101),
            'title': [f'Movie {i} (1995)' for i in range(1, 101)],
            'genres': ['Action|Adventure']*100
        })
        ratings = pd.DataFrame({
            'userId': [1]*100,
            'movieId': range(1, 101),
            'rating': np.random.uniform(3,5,100),
            'timestamp': [datetime.now()]*100
        })
        return movies, ratings, pd.DataFrame(), pd.DataFrame()

@st.cache_resource
def load_models(models_path):
    try:
        baseline = joblib.load(os.path.join(models_path, 'baseline_popularity.pkl'))
        best_model = joblib.load(os.path.join(models_path, 'lasso.pkl'))
        logistic = joblib.load(os.path.join(models_path, 'logistic_regression_model.pkl'))
        return baseline, best_model, logistic
    except:
        return None, None, None

BASE_PATH = "C:/Users/User/Downloads/ml-latest/ml-latest/output"   #adjust path as needed
MODELS_PATH = os.path.join(BASE_PATH, 'models')

movies, ratings, user_stats, genre_stats = load_data(BASE_PATH)
baseline_model, best_model, logistic = load_models(MODELS_PATH)

# Extract year
movies['year'] = movies['title'].apply(lambda x: re.search(r'\((\d{4})\)', str(x)).group(1) if re.search(r'\((\d{4})\)', str(x)) else None)
movies['clean_title'] = movies['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)

# Compute baseline weighted score if needed
if baseline_model is None:
    movie_stats = ratings.groupby('movieId').agg({'rating':['mean','count']}).reset_index()
    movie_stats.columns = ['movieId','avg_rating','vote_count']
    C = movie_stats['avg_rating'].mean()
    m = movie_stats['vote_count'].quantile(0.7)
    movie_stats['weighted_score'] = (movie_stats['vote_count']/(movie_stats['vote_count']+m))*movie_stats['avg_rating'] + (m/(movie_stats['vote_count']+m))*C
    movies = movies.merge(movie_stats, on='movieId', how='left')
else:
    movies = movies.merge(baseline_model['movie_scores'][['movieId','avg_rating','vote_count','weighted_score']], on='movieId', how='left')

movies['avg_rating'] = movies['avg_rating'].fillna(3.0)
movies['weighted_score'] = movies['weighted_score'].fillna(3.0)

# -------------------- SESSION STATE --------------------
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_movie' not in st.session_state: st.session_state.selected_movie = None

# -------------------- DISPLAY GRID --------------------
def display_movie_grid(movie_list, title="Movies", show_search=False, section_id="default"):
    """Display movies in a fixed-size grid with stable layout"""
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    cols_per_row = 6
    rows = [movie_list.iloc[i:i + cols_per_row] for i in range(0, len(movie_list), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, movie) in enumerate(row.iterrows()):
            with cols[idx]:
                poster_url = get_movie_poster(movie['title'], movie['year'])
                rating_display = f"{movie['avg_rating']:.1f}⭐" if pd.notna(movie['avg_rating']) else "N/A"

                # 🔒 FIXED-SIZE MOVIE CARD (NO st.image)
                st.markdown(f"""
                <div class="movie-card">
                    <div class="poster-container">
                        <img src="{poster_url}" />
                    </div>
                    <div class="movie-overlay">
                        <div class="movie-title">
                            {movie['clean_title'][:30]}{'...' if len(movie['clean_title']) > 30 else ''}
                        </div>
                        <div class="movie-year">
                            {movie['year'] if movie['year'] else 'N/A'} • {rating_display}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if show_search and st.button(
                    "Similar",
                    key=f"sim_{section_id}_{movie['movieId']}",
                    use_container_width=True
                ):
                    st.session_state.selected_movie = movie['movieId']
                    st.session_state.page = 'similar'
                    st.rerun()

# -------------------- COMBINED SCORE FUNCTION --------------------
def compute_recommendation_score(user_id, movie_df, ratings_df, baseline_model, lasso_model, logistic_model):
    if baseline_model is not None:
        movie_df = movie_df.merge(baseline_model['movie_scores'][['movieId','weighted_score']], on='movieId', how='left')
        movie_df['weighted_score'] = movie_df['weighted_score'].fillna(3.0)
    else:
        movie_df['weighted_score'] = 3.0

    if lasso_model is not None:
        X_lasso = movie_df[['avg_rating','vote_count']].fillna(3.0)
        movie_df['lasso_pred'] = lasso_model.predict(X_lasso)
    else:
        movie_df['lasso_pred'] = movie_df['avg_rating']

    if logistic_model is not None:
        X_logistic = movie_df[['avg_rating','vote_count']].fillna(3.0)
        movie_df['like_prob'] = logistic_model.predict_proba(X_logistic)[:,1]
    else:
        movie_df['like_prob'] = 0.5

    movie_df['final_score'] = 0.4*movie_df['weighted_score'] + 0.4*movie_df['lasso_pred'] + 0.2*(movie_df['like_prob']*5)
    return movie_df

# -------------------- HEADER & NAV --------------------
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1,3])
with col1: st.markdown('<div class="logo">StreamLens</div>', unsafe_allow_html=True)
with col2:
    search_col, button_col = st.columns([5,1])
    with search_col: search_query = st.text_input("Search", placeholder="Search movies...", label_visibility="collapsed", key="search")
    with button_col: search_button = st.button("Search", type="primary")

nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page='home'; st.rerun()
with nav_col2:
    if st.button("👤 Recommendations", use_container_width=True): st.session_state.page='recommendations'; st.rerun()
with nav_col3:
    if st.button("🔍 Search Movies", use_container_width=True): st.session_state.page='search'; st.rerun()
with nav_col4:
    if st.button("📊 Insights", use_container_width=True): st.session_state.page='insights'; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if search_query and search_button: st.session_state.page='search_results'; st.session_state.search_query=search_query

# -------------------- PAGES --------------------
if st.session_state.page == 'home':
    trending_movies = movies.sort_values('weighted_score', ascending=False).head(18)
    display_movie_grid(trending_movies, "Trending ", True, "home_trending")
    top_rated = movies.sort_values('avg_rating', ascending=False).head(18)
    display_movie_grid(top_rated, "⭐ Top Rated", show_search=True)
    if 'genres' in movies.columns:
        for genre in ['Action','Comedy','Drama','Thriller','Romance']:
            genre_movies = movies[movies['genres'].str.contains(genre, na=False)].sort_values('weighted_score', ascending=False).head(12)
            if len(genre_movies)>0: display_movie_grid(genre_movies, f"🎬 {genre} Movies", True, f"home_genre_{genre}")

elif st.session_state.page == 'recommendations':
    st.markdown('<div class="section-title">👤 Personalized Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="selection-panel">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        user_id = st.selectbox("Select User ID", options=sorted(ratings['userId'].unique()[:500]), help="Choose a user to see personalized recommendations")
    with col2:
        n_recommendations = st.slider("Number of Movies", min_value=6, max_value=36, value=18, step=6)
    with col3:
        genres_list = ['All Genres'] + sorted(set(g for sublist in movies['genres'].str.split('|').dropna() for g in sublist if g != '(no genres listed)'))
        genre_filter = st.selectbox("Genre Filter", genres_list)
    st.markdown('</div>', unsafe_allow_html=True)

    if user_id:
        user_ratings = ratings[ratings['userId']==user_id]
        watched_movies = set(user_ratings['movieId'])
        recommendations = movies[~movies['movieId'].isin(watched_movies)].copy()
        if genre_filter!='All Genres': recommendations = recommendations[recommendations['genres'].str.contains(genre_filter, na=False)]
        recommendations = compute_recommendation_score(user_id, recommendations, ratings, baseline_model, best_model, logistic)
        recommendations = recommendations.sort_values('final_score', ascending=False).head(n_recommendations)

        # User profile
        st.markdown('<div class="section-title">📊 User Profile</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f'<div class="insight-card"><div class="metric-value">{len(user_ratings)}</div><div class="metric-label">Movies Rated</div></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="insight-card"><div class="metric-value">{user_ratings["rating"].mean():.2f}⭐</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)
        with col3:
            top_genre = user_ratings.merge(movies, on='movieId')['genres'].str.split('|').explode().mode()
            top_genre_str = top_genre[0] if len(top_genre)>0 else 'N/A'
            st.markdown(f'<div class="insight-card"><div class="metric-value">{top_genre_str[:15]}</div><div class="metric-label">Favorite Genre</div></div>', unsafe_allow_html=True)
        with col4:
            rating_bias = "Generous" if user_ratings['rating'].mean()>3.5 else "Critical"
            st.markdown(f'<div class="insight-card"><div class="metric-value">{rating_bias}</div><div class="metric-label">Rating Style</div></div>', unsafe_allow_html=True)

        display_movie_grid(recommendations, f"🎯 Recommended for User {user_id}")

# -------------------- SEARCH & SIMILAR --------------------
elif st.session_state.page in ['search','search_results']:
    st.markdown('<div class="section-title">🔍 Search & Discover</div>', unsafe_allow_html=True)
    query = st.session_state.search_query if st.session_state.page=='search_results' and 'search_query' in st.session_state else st.text_input("Search for movies","Enter movie title...")
    if query:
        search_results = movies[movies['title'].str.contains(query, case=False, na=False)].copy()
        search_results = compute_recommendation_score(None, search_results, ratings, baseline_model, best_model, logistic)
        search_results = search_results.sort_values('final_score', ascending=False).head(24)
        if len(search_results)>0: display_movie_grid(search_results, f"Search Results: '{query}'", show_search=True)
        else: st.warning("No movies found. Try a different search term.")

elif st.session_state.page=='similar' and st.session_state.selected_movie:
    selected = movies[movies['movieId']==st.session_state.selected_movie].iloc[0]
    st.markdown(f'<div class="section-title">🎬 Similar to: {selected["title"]}</div>', unsafe_allow_html=True)
    movie_genres = set(selected['genres'].split('|'))
    similar_movies = movies[movies['movieId']!=st.session_state.selected_movie].copy()
    similar_movies['similarity'] = similar_movies['genres'].apply(lambda x: len(set(x.split('|')) & movie_genres)/len(movie_genres) if pd.notna(x) else 0)
    similar_movies = similar_movies[similar_movies['similarity']>0]
    similar_movies = compute_recommendation_score(None, similar_movies, ratings, baseline_model, best_model, logistic)
    similar_movies = similar_movies.sort_values(['similarity','final_score'], ascending=[False,False]).head(24)
    display_movie_grid(similar_movies, "🎯 Movies You Might Like", show_search=True)

# -------------------- INSIGHTS --------------------
elif st.session_state.page=='insights':
    st.markdown('<div class="section-title">📊 Business Insights Dashboard</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="insight-card"><div class="metric-value">{len(movies):,}</div><div class="metric-label">Total Movies</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="insight-card"><div class="metric-value">{len(ratings):,}</div><div class="metric-label">Total Ratings</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="insight-card"><div class="metric-value">{ratings["userId"].nunique():,}</div><div class="metric-label">Active Users</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="insight-card"><div class="metric-value">{ratings["rating"].mean():.2f}⭐</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)

    if genre_stats is not None and not genre_stats.empty:
        st.markdown('<div class="section-title">🎭 Genre Performance</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(genre_stats.sort_values('avg_rating', ascending=False).head(10), x='avg_rating', y='genre', orientation='h', title='Top 10 Genres by Rating', color='avg_rating', color_continuous_scale='RdYlGn', template='plotly_dark')
            fig1.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f'); st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.bar(genre_stats.sort_values('n_ratings', ascending=False).head(10), x='n_ratings', y='genre', orientation='h', title='Top 10 Most Popular Genres', color='n_ratings', color_continuous_scale='Blues', template='plotly_dark')
            fig2.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f'); st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">📈 Rating Distribution</div>', unsafe_allow_html=True)
    fig3 = px.histogram(ratings, x='rating', nbins=10, title='Distribution of Ratings', color_discrete_sequence=['#e50914'], template='plotly_dark')
    fig3.update_layout(plot_bgcolor='#1f1f1f', paper_bgcolor='#1f1f1f'); st.plotly_chart(fig3, use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""<div style='text-align: center; color: #666; padding: 40px;'>
    <p style='font-size: 0.9rem;'>StreamRec - Powered by MovieLens & TMDb</p>
    <p style='font-size: 0.8rem;'>ML Recommendation System • December 2025</p>
</div>""", unsafe_allow_html=True)

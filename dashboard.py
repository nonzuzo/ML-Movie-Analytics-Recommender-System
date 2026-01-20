import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="MovieLens Strategic Dashboard", page_icon="🎬", layout="wide")

# CSS FOR STYLING 
st.markdown("""
    <style>
        .block-container {padding-top: 1rem;}
        div[data-testid="stMetricValue"] {font-size: 1.5rem;}
        .stAlert {padding: 0.5rem;}
    </style>
""", unsafe_allow_html=True)

def generate_mock_data():
    """Generates robust dummy data for the dashboard."""
    # 1. User Stats
    users = pd.DataFrame({
        'user_id': range(1, 1001),
        'n_ratings': np.random.randint(1, 200, 1000),
        'rating_bias': np.random.choice(['Generous', 'Neutral', 'Harsh'], 1000, p=[0.2, 0.6, 0.2])
    })
    
    # 2. Trends
    dates = pd.date_range(start='2020-01-01', periods=36, freq='M')
    trends = pd.DataFrame({
        'year_month': dates.astype(str),
        'avg_rating': np.random.uniform(3.0, 4.5, 36)
    })

    # 3. Genre Performance
    genres_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Thriller', 'Animation']
    genres = pd.DataFrame({
        'genre': genres_list,
        'n_ratings': np.random.randint(500, 5000, len(genres_list)),
        'avg_rating': np.random.uniform(2.5, 4.8, len(genres_list))
    })

    # 4. Tags
    tags = pd.DataFrame({
        'tag': ['funny', 'dark', 'surreal', 'twist ending', 'boring', 'classic', 'emotional', 'scary'] * 10,
        'n_uses': np.random.randint(10, 100, 80),
        'avg_rating': np.random.uniform(1.5, 5.0, 80)
    })

    # 5. Hidden Gems (Expanded for Recommendations)
    titles = [f'Movie {i}' for i in range(200)]
    gems = pd.DataFrame({
        'title': titles,
        'release_year': np.random.randint(1980, 2024, 200),
        'genres': np.random.choice(genres_list, 200),
        'avg_rating': np.random.uniform(2.0, 5.0, 200),
        'n_ratings': np.random.randint(10, 1000, 200) 
    })

    # 6. Decades
    decades = pd.DataFrame({
        'decade': [1980, 1990, 2000, 2010, 2020],
        'avg_rating_mean': np.random.uniform(3.2, 4.2, 5),
        'n_movies_rated': np.random.randint(1000, 10000, 5)
    })
    
    return users, trends, genres, tags, gems, decades

@st.cache_data
def load_data():
    folder = 'MovieLens_Dashboard_Data/' 
    try:
        users = pd.read_csv(folder + 'user_stats.csv')
        trends = pd.read_csv(folder + 'rating_trends.csv')
        genres = pd.read_csv(folder + 'genre_performance.csv')
        tags = pd.read_csv(folder + 'tag_analysis.csv')
        gems = pd.read_csv(folder + 'hidden_gems.csv')
        decades = pd.read_csv(folder + 'decade_impact.csv')
        data_source = "Local Files"
    except FileNotFoundError:
        users, trends, genres, tags, gems, decades = generate_mock_data()
        data_source = "Mock Data (Files not found)"

    # Data Cleaning
    gems['release_year'] = pd.to_numeric(gems['release_year'], errors='coerce').fillna(2000).astype(int)
    
    # Feature Engineering for Heatmap
    if 'decade' not in gems.columns:
        gems['decade'] = (gems['release_year'] // 10) * 10

    return users, trends, genres, tags, gems, decades, data_source

df_users, df_trends, df_genres, df_tags, df_gems, df_decades, source = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to", 
    ["User Behavior", "Content Insights", "Hidden Patterns", "Movie Recommender"]
)

st.sidebar.markdown("---")
st.sidebar.header("Global Filters")

# Fixed: Slider is now always visible regardless of page
min_votes = st.sidebar.slider("Min Ratings (for Genre/Tag charts)", 100, 5000, 500)

if source.startswith("Mock"):
    st.sidebar.warning(f"Using {source}")

# --- MAIN PAGE HEADER ---
st.title("MovieLens Business Intelligence")
st.markdown(f"**Current View:** {page}")
st.markdown("---")


# PAGE 1: USER BEHAVIOR

if page == "User Behavior":
    
    col1, col2, col3 = st.columns(3)
    
    generous_count = len(df_users[df_users['rating_bias'] == 'Generous'])
    harsh_count = len(df_users[df_users['rating_bias'] == 'Harsh'])
    total_users = len(df_users)
    
    col1.metric("Generous Raters", f"{generous_count:,}", f"{(generous_count/total_users)*100:.1f}%")
    col2.metric("Harsh Raters", f"{harsh_count:,}", f"{(harsh_count/total_users)*100:.1f}%")
    col3.metric("Total Users", f"{total_users:,}")
    
    st.markdown("### Deep Dive")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Rating Activity")
        df_trends = df_trends.sort_values('year_month')
        fig_trend = px.line(df_trends, x='year_month', y='avg_rating', markers=True, title="Avg Rating Over Time")
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        st.subheader("User Retention Tiers")
        bins = [0, 1, 19, 99, 100000]
        labels = ['One-Time', 'Casual', 'Active', 'Power User']
        df_users['tier'] = pd.cut(df_users['n_ratings'], bins=bins, labels=labels)
        
        retention_counts = df_users['tier'].value_counts().reset_index()
        retention_counts.columns = ['User Tier', 'Count']
        
        fig_ret = px.bar(retention_counts, x='User Tier', y='Count', color='User Tier',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_ret, use_container_width=True)


# PAGE 2: CONTENT INSIGHTS

elif page == "Content Insights":
    
    active_genres = df_genres[df_genres['n_ratings'] >= min_votes].sort_values('avg_rating')
    
    if active_genres.empty:
        st.warning("No genres meet the filter criteria.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Highest Rated Genres")
            fig_best = px.bar(active_genres.tail(10), x='avg_rating', y='genre', orientation='h', 
                              color='avg_rating', color_continuous_scale='Bluered')
            st.plotly_chart(fig_best, use_container_width=True)
        with col2:
            st.subheader("Lowest Rated Genres")
            fig_worst = px.bar(active_genres.head(10), x='avg_rating', y='genre', orientation='h', 
                               color='avg_rating', color_continuous_scale='Redor_r')
            st.plotly_chart(fig_worst, use_container_width=True)

    st.subheader("Tag Sentiment Analysis")
    valid_tags = df_tags[df_tags['n_uses'] >= 10] 
    
    if not valid_tags.empty:
        fig_tags = px.scatter(valid_tags, x='n_uses', y='avg_rating', hover_data=['tag'], size='n_uses',
                              color='avg_rating', title="Tag Popularity vs. Rating")
        fig_tags.add_hline(y=3.5, line_dash="dash", annotation_text="Avg Threshold")
        st.plotly_chart(fig_tags, use_container_width=True)
    else:
        st.info("Not enough tag data.")


# PAGE 3: HIDDEN PATTERNS

elif page == "Hidden Patterns":
    
    st.subheader("Decade vs. Genre Heatmap")
    st.markdown("Which genres dominated specific decades?")
    
    # Create pivot table for heatmap
    # Ensuring we have 'decade' column
    if 'decade' not in df_gems.columns:
        df_gems['decade'] = (df_gems['release_year'] // 10) * 10
        
    heatmap_data = df_gems.pivot_table(index='genres', columns='decade', values='avg_rating', aggfunc='mean')
    
    if not heatmap_data.empty:
        fig_heat = px.imshow(heatmap_data, 
                             labels=dict(x="Decade", y="Genre", color="Avg Rating"),
                             color_continuous_scale="Viridis",
                             text_auto=".1f")
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.warning("Not enough data to generate heatmap.")

    st.markdown("---")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Historical Rating Trends")
        fig_years = px.scatter(df_decades, x='decade', y='avg_rating_mean', size='n_movies_rated', 
                               color='avg_rating_mean', size_max=60)
        st.plotly_chart(fig_years, use_container_width=True)
    with c2:
        st.subheader("Golden Era")
        if not df_decades.empty:
            golden = df_decades.loc[df_decades['avg_rating_mean'].idxmax()]
            st.success(f"Best Decade: **{int(golden['decade'])}s**")
            st.metric("Avg Rating", f"{golden['avg_rating_mean']:.2f}")


# PAGE 4: MOVIERECOMMENDER 

elif page == "Movie Recommender":
    st.header("Find Your Next Movie")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # Get unique genres
        unique_genres = sorted(list(set(df_gems['genres'].astype(str).str.split('|').explode().dropna().unique())))
        selected_genre = st.selectbox("1. Preferred Genre", unique_genres)
        
    with c2:
        # Vibe based on popularity (n_ratings)
        vibe = st.select_slider("2. The Vibe", options=["Hidden Gem", "Cult Classic", "Mainstream Hit"])
        
    with c3:
        # Decade filter
        decades = sorted(df_gems['decade'].unique())
        selected_decade = st.selectbox("3. Preferred Decade", decades, index=len(decades)-1)

    # --- RECOMMENDATION LOGIC ---
    # 1. Filter by Genre and Decade
    rec_pool = df_gems[
        (df_gems['genres'].str.contains(selected_genre, na=False)) & 
        (df_gems['decade'] == selected_decade)
    ].copy()
    
    # 2. Filter by Vibe (using n_ratings percentiles)
    if not rec_pool.empty:
        low_bound = rec_pool['n_ratings'].quantile(0.33)
        high_bound = rec_pool['n_ratings'].quantile(0.66)
        
        if vibe == "Hidden Gem":
            rec_pool = rec_pool[rec_pool['n_ratings'] <= low_bound]
        elif vibe == "Cult Classic":
            rec_pool = rec_pool[(rec_pool['n_ratings'] > low_bound) & (rec_pool['n_ratings'] <= high_bound)]
        else: # Mainstream Hit
            rec_pool = rec_pool[rec_pool['n_ratings'] > high_bound]
            
    st.markdown("---")
    
    if rec_pool.empty:
        st.warning(f"No {vibe} {selected_genre} movies found from the {selected_decade}s. Try changing the settings!")
    else:
        st.subheader(f"Top Picks: {vibe} {selected_genre} ({selected_decade}s)")
        
        # Sort by rating and take top 3
        top_picks = rec_pool.sort_values('avg_rating', ascending=False).head(3)
        
        cols = st.columns(3)
        for idx, (_, row) in enumerate(top_picks.iterrows()):
            with cols[idx]:
                st.info(f"**{row['title']}** ({row['release_year']})")
                st.metric("Rating", f"⭐ {row['avg_rating']:.1f}")
                st.caption(f"Based on {row['n_ratings']} user votes")
                
                # Dynamic "Why watch" text
                if row['avg_rating'] > 4.5:
                    st.write("**Must Watch:** Universally acclaimed.")
                elif vibe == "Hidden Gem":
                    st.write("**Underrated:** Great quality, few ratings.")
                else:
                    st.write("**Solid Pick:** Fits your criteria perfectly.")
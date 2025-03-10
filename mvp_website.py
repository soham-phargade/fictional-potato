import os
import psycopg2
import streamlit as st
import pandas as pd

# Database connection parameters
DB_PARAMS = {
    "dbname": "article_db",
    "user": "postgres",
    "password": os.getenv("PGPASSWORD"),
    "host": "localhost",
    "port": "5432",
}

# Function to fetch top 20 articles
def get_top_articles():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        query = """
        SELECT title, url, image_url, engagement_score 
        FROM articles 
        ORDER BY engagement_score DESC 
        LIMIT 20;
        """
        cur.execute(query)
        articles = cur.fetchall()
        cur.close()
        conn.close()
        return articles
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return []

# Streamlit UI
st.set_page_config(page_title="Top Articles", layout="wide")
st.title("Top 20 Articles by Engagement Score")

articles = get_top_articles()

if not articles:
    st.write("No articles found.")
else:
    # Grid layout: 2 columns per row
    cols = st.columns(2)
    for idx, (title, url, image_url, engagement_score) in enumerate(articles):
        with cols[idx % 2]:
            st.markdown(f"### [{title}]({url})")
            if image_url:
                st.markdown(f'<a href="{url}" target="_blank"><img src="{image_url}" width="100%"></a>', unsafe_allow_html=True)
            st.markdown(f"<small>Engagement Score: {engagement_score}</small>", unsafe_allow_html=True)
            st.write("---")

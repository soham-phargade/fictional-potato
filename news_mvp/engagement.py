import os
import psycopg2
import pandas as pd
import numpy as np
import gensim
import gensim.corpora as corpora
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk

# Download necessary NLTK resources
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

# Database connection details
DB_PARAMS = {
    "dbname": "article_db",
    "user": "postgres",
    "password": os.getenv("PGPASSWORD"),
    "host": "localhost",
    "port": "5432",
}

def get_articles():
    """Fetches articles from the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        query = "SELECT id, title, content FROM articles;"
        cur.execute(query)
        articles = cur.fetchall()
        cur.close()
        conn.close()
        return articles
    except Exception as e:
        print("Error fetching articles:", e)
        return []

def preprocess_text(text):
    """Tokenizes, removes stopwords, and cleans text."""
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return tokens

def compute_lexical_diversity(tokens):
    """Computes lexical diversity (Type-Token Ratio)."""
    if len(tokens) == 0:
        return 0
    unique_tokens = set(tokens)
    return len(unique_tokens) / len(tokens)

def perform_topic_modeling(processed_articles):
    """Applies LDA topic modeling to articles."""
    dictionary = corpora.Dictionary(processed_articles)
    corpus = [dictionary.doc2bow(text) for text in processed_articles]
    lda_model = gensim.models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)
    
    # Assign topic scores to each article
    topic_scores = []
    for bow in corpus:
        topics = lda_model.get_document_topics(bow)
        max_topic = max(topics, key=lambda x: x[1])[1] if topics else 0
        topic_scores.append(max_topic)

    return topic_scores

def update_database(article_scores):
    """Updates the database with engagement scores."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        update_query = """
        UPDATE articles
        SET lexical_diversity = %s, topic_score = %s, engagement_score = %s
        WHERE id = %s;
        """

        # Convert numpy floats to Python floats before executing
        article_scores = [(float(ld), float(ts), float(es), article_id) for ld, ts, es, article_id in article_scores]

        cur.executemany(update_query, article_scores)
        conn.commit()
        cur.close()
        conn.close()
        print("Database updated successfully!")

    except Exception as e:
        print("Error updating database:", e)

# Fetch articles from the database
articles = get_articles()

# Preprocess articles
article_texts = [preprocess_text(title + " " + content) for _, title, content in articles]

# Compute lexical diversity for each article
lexical_diversities = [compute_lexical_diversity(text) for text in article_texts]

# Perform topic modeling and get topic scores
topic_scores = perform_topic_modeling(article_texts)

# Compute final engagement score (weighted sum)
engagement_scores = [ld * 0.5 + ts * 0.5 for ld, ts in zip(lexical_diversities, topic_scores)]

# Prepare data for DB update
article_scores = [(ld, ts, es, article_id) for (article_id, _, _), ld, ts, es in zip(articles, lexical_diversities, topic_scores, engagement_scores)]

# Update database with computed scores
update_database(article_scores)

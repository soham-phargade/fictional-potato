import os
import re
import csv
from newspaper import Article
import psycopg2
import traceback

# Database connection
try:
    conn = psycopg2.connect(
        dbname="article_db",
        user="postgres",
        password=os.getenv("PGPASSWORD"),
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connected to PostgreSQL")
except Exception as e:
    print("An error occurred connecting to DB:", e)
    print(traceback.format_exc())
    exit(1)

# Read URLs from the CSV file
csv_file = "tech_news.csv"
try:
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        urls = [row[0].strip() for row in reader if row]
except Exception as e:
    print("Error reading CSV file:", e)
    exit(1)

# Process each URL
try:
    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            safe_title = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_')[:50]

            # Check if the article exists
            cur.execute("SELECT 1 FROM articles WHERE url = %s;", (url,))
            exists = cur.fetchone()
            
            if not exists:
                cur.execute(
                    "INSERT INTO articles (url, title, content, image_url) VALUES (%s, %s, %s, %s);",
                    (url, article.title, article.text, article.top_image)
                )
                conn.commit()
                print(f"Saved: {article.title}")
            else:
                print(f"Already exists: {article.title}")
        
        except Exception as e:
            print("Error occurred scraping the URL:", url, e)
            continue

except KeyboardInterrupt:
    print("\nUser interrupted. Exiting gracefully...")

finally:
    if conn:
        cur.close()
        conn.close()
        print("Database connection closed.")

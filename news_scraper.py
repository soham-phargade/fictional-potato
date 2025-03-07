import os
import re
from newspaper import Article
import psycopg2
import traceback

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
    print("An error occured connecting to DB:", e)
    print(traceback.format_exc())

try:
    while True:
        try:
            url = input("Enter an article URL ('exit' to quit): ").strip()
            if(url.lower() == "exit" or url == "quit"): break

            
            article = Article(url)
            article.download()
            article.parse()
            safe_title = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_')[:50]

            # Save the article
            cur.execute("SELECT 1 FROM articles WHERE url = %s;", (url,))
            exists = cur.fetchone() # None if doesn't exist in DB
            if(not exists):
                cur.execute(
                    "INSERT INTO articles (url, title, content, image_url) VALUES (%s, %s, %s, %s);",
                        (url, article.title, article.text, article.top_image)
                    )
            conn.commit()
        except Exception as e:
            print("Error occured scraping the URL:", e)
            #print(traceback.format_exc())

except KeyboardInterrupt:
    print("\nUser interrupted. Exiting gracefully...")

finally:
    if conn:
        cur.close()
        conn.close()
        print("Database connection closed.")
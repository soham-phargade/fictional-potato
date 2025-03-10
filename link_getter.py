import feedparser
import csv
from datetime import datetime

# List of high-quality tech news RSS feeds
RSS_FEEDS = [
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://www.theverge.com/rss/index.xml",
    "https://www.cnet.com/rss/news/",
]

# Output CSV file
CSV_FILE = "tech_news.csv"

def fetch_news():
    articles = []
    # today = datetime.today().strftime('%Y-%m-%d')

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            articles.append([entry.link])
            # article_date = entry.published[:10]  # Extract YYYY-MM-DD
            # if article_date == today:
            #     articles.append([entry.title, entry.link, article_date])

    return articles

def save_to_csv(articles):
    # Write data to CSV file
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # writer.writerow(["Link"])  # Header row
        writer.writerows(articles)

def main():
    articles = fetch_news()
    if articles:
        save_to_csv(articles)
        print(f"✅ {len(articles)} new articles saved to {CSV_FILE}")
    else:
        print("⚠ No new articles found today.")

if __name__ == "__main__":
    main()

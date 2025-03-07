import os
import re
from newspaper import Article

while(1):
    url = input("Enter an article: ")
    if(url == "exit" or url == "quit"): break

    article = Article(url)
    article.download()
    article.parse()

    # Create output folder
    os.makedirs("output", exist_ok=True)

    # Sanitize filename (remove special chars, replace spaces with underscores)
    safe_title = re.sub(r'[^\w\s-]', '', article.title).strip().replace(' ', '_')[:50]

    # Save the article
    with open(f"output/{safe_title}.txt", "w", encoding="utf-8") as f:
        f.write(f"Title: {article.title}\n\n{article.text}\n\nImage: {article.top_image}")

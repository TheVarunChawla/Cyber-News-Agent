import feedparser

feeds = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Cybersecurity Dive": "https://www.cybersecuritydive.com/feeds/news/",
    "Trend Micro": "https://www.trendmicro.com/rss/index.xml"
}

output = "# Daily Cyber News\n\n"

for source, url in feeds.items():

    feed = feedparser.parse(url)

    output += f"## {source}\n\n"

    for article in feed.entries[:5]:

        output += f"### {article.title}\n"
        output += f"{article.link}\n\n"

with open("daily_news.md", "w", encoding="utf-8") as f:
    f.write(output)

print("News file generated successfully!")

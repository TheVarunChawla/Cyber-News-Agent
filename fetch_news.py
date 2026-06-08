import feedparser

feeds = {

    # Threat Intelligence
    "The Hacker News":
        "https://feeds.feedburner.com/TheHackersNews",

    "BleepingComputer":
        "https://www.bleepingcomputer.com/feed/",

    "Cybersecurity Dive":
        "https://www.cybersecuritydive.com/feeds/news/",

    "Trend Micro":
        "https://www.trendmicro.com/rss/index.xml",

    # Government

    "CISA":
        "https://www.cisa.gov/news.xml",

    # Vendor Threat Research

    "Palo Alto Unit42":
        "https://unit42.paloaltonetworks.com/feed/",

    "Cisco Talos":
        "https://blog.talosintelligence.com/rss/",

    "Microsoft Security Response Center":
        "https://msrc.microsoft.com/blog/feed",

    "Google Security Blog":
        "https://security.googleblog.com/feeds/posts/default"

}

output = "# Daily Cyber News\n\n"

for source, url in feeds.items():

    feed = feedparser.parse(url)

    output += f"## {source}\n\n"

    for article in feed.entries[:5]:

        output += f"### {article.title}\n\n"

if hasattr(article, "published"):
    output += f"Published: {article.published}\n\n"

if hasattr(article, "summary"):
    summary = article.summary.replace("<p>", "").replace("</p>", "")
    summary = summary.replace("<br />", "")
    output += f"Summary:\n{summary}\n\n"

output += f"URL:\n{article.link}\n\n"

output += "--------------------------------------------\n\n"

with open("daily_news.md", "w", encoding="utf-8") as f:
    f.write(output)

print("News file generated successfully!")

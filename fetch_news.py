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
        "https://security.googleblog.com/feeds/posts/default",

    "Microsoft Security Blog":
        "https://www.microsoft.com/en-us/security/blog/feed/"
}

skip_words = [
    "sponsored",
    "webinar",
    "podcast",
    "advertisement"
]

output = "# Daily Cyber Intelligence\n\n"

for source, url in feeds.items():

    output += "=" * 60 + "\n"
    output += f"SOURCE : {source}\n"
    output += "=" * 60 + "\n\n"

    feed = feedparser.parse(url)

    for article in feed.entries[:3]:

        title = article.title.lower()

        if any(word in title for word in skip_words):
            continue

        output += f"Title:\n{article.title}\n\n"

        if hasattr(article, "published"):
            output += f"Published:\n{article.published}\n\n"

        if hasattr(article, "summary"):

            summary = article.summary

            summary = summary.replace("<p>", "")
            summary = summary.replace("</p>", "")
            summary = summary.replace("<br />", "")
            summary = summary.replace("&nbsp;", " ")

            output += f"Summary:\n{summary}\n\n"

        output += f"URL:\n{article.link}\n\n"

        output += "-" * 60 + "\n\n"

with open("daily_news.md", "w", encoding="utf-8") as f:
    f.write(output)

print("Daily Cyber Intelligence file generated successfully!")

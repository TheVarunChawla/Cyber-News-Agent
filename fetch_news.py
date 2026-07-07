import feedparser
from datetime import datetime, timezone, timedelta
from time import mktime

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

# How far back to look for "fresh" articles. If a feed has nothing this
# recent, we fall back to its latest items so a slow-news day doesn't
# leave that section empty.
LOOKBACK_HOURS = 48
MAX_PER_FEED = 5

now_utc = datetime.now(timezone.utc)
run_timestamp = now_utc.strftime("%Y-%m-%d %H:%M UTC")

output = "# Daily Cyber Intelligence\n\n"
output += f"_Last run: {run_timestamp}_\n\n"

any_fresh_found = False
feed_errors = []

for source, url in feeds.items():

    output += "=" * 60 + "\n"
    output += f"SOURCE : {source}\n"
    output += "=" * 60 + "\n\n"

    try:
        feed = feedparser.parse(url)
    except Exception as e:
        feed_errors.append(f"{source}: {e}")
        output += f"[Could not fetch this feed: {e}]\n\n"
        continue

    # feedparser doesn't always raise on failure - it can just return
    # an object with no entries and a populated 'bozo_exception'.
    if getattr(feed, "bozo", 0) and not feed.entries:
        err = getattr(feed, "bozo_exception", "unknown parsing error")
        feed_errors.append(f"{source}: {err}")
        output += f"[Feed error, no entries returned: {err}]\n\n"
        continue

    if not feed.entries:
        output += "[No entries returned from this feed]\n\n"
        continue

    # Split entries into "fresh" (within lookback window) vs everything else
    fresh = []
    fallback = []

    for article in feed.entries:
        title = article.title.lower() if hasattr(article, "title") else ""

        if any(word in title for word in skip_words):
            continue

        published_dt = None
        if hasattr(article, "published_parsed") and article.published_parsed:
            published_dt = datetime.fromtimestamp(
                mktime(article.published_parsed), tz=timezone.utc
            )

        if published_dt and (now_utc - published_dt) <= timedelta(hours=LOOKBACK_HOURS):
            fresh.append((article, published_dt))
        else:
            fallback.append((article, published_dt))

    chosen = fresh[:MAX_PER_FEED]
    used_fallback = False

    if chosen:
        any_fresh_found = True
    else:
        # Nothing fresh - fall back to the latest available items so the
        # section isn't blank, but flag it clearly.
        chosen = fallback[:3]
        used_fallback = True

    if used_fallback:
        output += f"[No articles in the last {LOOKBACK_HOURS}h - showing latest available]\n\n"

    if not chosen:
        output += "[No usable entries after filtering]\n\n"
        continue

    for article, published_dt in chosen:

        output += f"Title:\n{article.title}\n\n"

        if published_dt:
            output += f"Published:\n{published_dt.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        elif hasattr(article, "published"):
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

if feed_errors:
    output += "=" * 60 + "\n"
    output += "FEED ERRORS THIS RUN\n"
    output += "=" * 60 + "\n\n"
    for err in feed_errors:
        output += f"- {err}\n"
    output += "\n"

with open("daily_news.md", "w", encoding="utf-8") as f:
    f.write(output)

print("Daily Cyber Intelligence file generated successfully!")
if feed_errors:
    print(f"Warning: {len(feed_errors)} feed(s) had errors: {feed_errors}")

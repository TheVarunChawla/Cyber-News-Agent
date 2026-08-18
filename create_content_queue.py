"""Create one human-reviewed LinkedIn learning-post brief per scheduled run."""

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LIBRARY_FILE = ROOT / "content_library.json"
HISTORY_FILE = ROOT / "content_history.json"
NEWS_FILE = ROOT / "daily_news.md"
QUEUE_FILE = ROOT / "content_queue.md"
RECENT_TOPIC_DAYS = 42


def load_json(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def recent_slugs(history, today):
    recent = set()
    for entry in history.get("published_topics", []):
        try:
            used_on = date.fromisoformat(entry["date"])
        except (KeyError, ValueError):
            continue
        if (today - used_on).days < RECENT_TOPIC_DAYS:
            recent.add(entry.get("slug"))
    return recent


def news_titles():
    if not NEWS_FILE.exists():
        return []
    content = NEWS_FILE.read_text(encoding="utf-8")
    return re.findall(r"^Title:\s*\n(.+)$", content, flags=re.MULTILINE)


def related_news(topic, titles):
    keywords = [keyword.lower() for keyword in topic["keywords"]]
    matches = [title for title in titles if any(word in title.lower() for word in keywords)]
    return matches[:2]


def choose_topic(library, used_slugs, today):
    available = [topic for topic in library if topic["slug"] not in used_slugs]
    # A small library may be exhausted before the 42-day no-repeat window.
    # Reuse it gracefully rather than failing the scheduled workflow.
    if not available:
        available = library
    # The date makes selection predictable and keeps the library rotation fair.
    return available[today.toordinal() % len(available)]


def make_caption(topic, context_titles):
    caption = f"{topic['hook']}\n\n{topic['explanation']}\n\n"
    caption += f"What to remember: {topic['takeaway']}\n\n"
    if context_titles:
        caption += "Why this is timely: a recent security story made this concept relevant again. "
        caption += "Use the news as supporting context—not as the whole post.\n\n"
    caption += "What part of this topic would you like me to explain next?\n\n"
    caption += " ".join(f"#{tag}" for tag in topic["hashtags"])
    return caption


def write_queue(topic, titles, run_time):
    related = related_news(topic, titles)
    carousel = "\n".join(f"{number}. {slide}" for number, slide in enumerate(topic["carousel"], 1))
    news_section = "\n".join(f"- {title}" for title in related) or "- No matching story needed; this is an evergreen learning post."
    output = f"""# LinkedIn Content Queue

_Generated: {run_time}_

## This post's topic

**{topic['title']}**

## Format recommendation

Use one of these; do not create all three for the same topic.

- **Fastest:** a single image using this visual brief: {topic['visual']}
- **Best for saves:** a 5-slide PDF carousel:
{carousel}
- **Most eye-catching:** a 5–8 second looping GIF: {topic['gif']}

## Ready-to-personalize LinkedIn caption

{make_caption(topic, related)}

## Optional current-event context

{news_section}

## Before publishing

- Add one personal line from your SOC, training, or learning experience.
- Check every technical claim against a reliable source before posting.
- Choose one visual format and keep the post focused on this one concept.
- Reply to early comments with helpful explanations; this is part of the content, not an afterthought.
"""
    QUEUE_FILE.write_text(output, encoding="utf-8")


def main():
    library = load_json(LIBRARY_FILE, [])
    if not library:
        raise RuntimeError("content_library.json has no topics")

    history = load_json(HISTORY_FILE, {"published_topics": []})
    today = date.today()
    topic = choose_topic(library, recent_slugs(history, today), today)
    write_queue(topic, news_titles(), datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))

    history.setdefault("published_topics", []).append({"date": today.isoformat(), "slug": topic["slug"]})
    history["published_topics"] = history["published_topics"][-100:]
    HISTORY_FILE.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    print(f"Content queue created for: {topic['title']}")


if __name__ == "__main__":
    main()

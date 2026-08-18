# Cyber Learning Content Queue

This project helps create **three human-reviewed LinkedIn cybersecurity learning posts per week**. It is intentionally not an auto-poster.

## What happens on Monday, Wednesday, and Friday

1. `fetch_news.py` collects current cybersecurity headlines as optional context.
2. `create_content_queue.py` rotates through an evergreen cybersecurity concept.
3. It writes `content_queue.md` with:
   - one clear concept and a simple hook;
   - a ready-to-personalize LinkedIn caption;
   - a single-image brief, PDF-carousel outline, and GIF idea;
   - matching current news only when it genuinely adds context.
4. GitHub Actions commits the queue. Review it, add your own point of view, make the visual, and publish manually.

## Why this is different

News is input, not the final product. The content library prioritizes concepts that people can understand, save, and share: phishing, MFA, VPNs, patching, encryption, SIEM, ransomware, Zero Trust, and EDR.

## Personalise the output

Edit `content_library.json` to add topics in your voice. Each topic has the hook, explanation, takeaway, visual brief, carousel slides, GIF idea, current-news keywords, and hashtags.

Before you publish, add a genuine personal line: something you observed in a SOC, learned while studying, or recommend that a beginner practise. Verify technical claims and source any current-event references.

## Run it locally

```powershell
pip install -r requirements.txt
python fetch_news.py
python create_content_queue.py
```

Then open `content_queue.md`.

#!/usr/bin/env python3
"""
Generate RSS podcast feeds for NRJ Paris and NRJ Belgique.
Feeds point to the current week's Monday 00h recording.
Run every Monday just after midnight (UTC+1 Paris time).
"""

from datetime import datetime, timezone, timedelta
import os

# Paris/Brussels timezone = UTC+1 (UTC+2 in summer, but we keep it simple)
# GitHub Actions will run at 23:05 UTC Sunday = 00:05 Monday Paris time
PARIS_TZ = timezone(timedelta(hours=1))

now = datetime.now(PARIS_TZ)

# Format for RSS pub date
pub_date = now.strftime("%a, %d %b %Y 00:00:00 +0100")

# ISO date for episode guid (unique per week)
week_label = now.strftime("%Y-W%W")  # e.g. 2026-W12

# GitHub Pages base URL — update this after creating the repo
GITHUB_USER = "YOUR_GITHUB_USERNAME"
GITHUB_REPO = "nrj-rss"
BASE_URL = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"

feeds = [
    {
        "filename": "nrj-paris.xml",
        "title": "NRJ Paris",
        "description": "Enregistrement hebdomadaire NRJ Paris — lundi 00h",
        "image": "https://upload.wikimedia.org/wikipedia/fr/thumb/6/6e/NRJ_logo_2019.svg/1200px-NRJ_logo_2019.svg.png",
        "audio_url": "https://piges.alexandremartinat.com/NRJ_Paris/Monday/00.mp3",
        "audio_type": "audio/mpeg",
        "guid_prefix": "nrj-paris",
    },
    {
        "filename": "nrj-belgique.xml",
        "title": "NRJ Belgique",
        "description": "Enregistrement hebdomadaire NRJ Belgique — lundi 00h",
        "image": "https://upload.wikimedia.org/wikipedia/fr/thumb/6/6e/NRJ_logo_2019.svg/1200px-NRJ_logo_2019.svg.png",
        "audio_url": "https://piges.alexandremartinat.com/NRJ_Belgique/Monday/00.aac",
        "audio_type": "audio/aac",
        "guid_prefix": "nrj-belgique",
    },
]

os.makedirs("feeds", exist_ok=True)

for feed in feeds:
    guid = f"{feed['guid_prefix']}-{week_label}"
    feed_url = f"{BASE_URL}/feeds/{feed['filename']}"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{feed['title']}</title>
    <link>{BASE_URL}</link>
    <description>{feed['description']}</description>
    <language>fr</language>
    <lastBuildDate>{pub_date}</lastBuildDate>
    <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>
    <itunes:author>NRJ</itunes:author>
    <itunes:image href="{feed['image']}"/>
    <itunes:category text="Music"/>
    <itunes:explicit>false</itunes:explicit>

    <item>
      <title>{feed['title']} — semaine du {now.strftime('%d/%m/%Y')}</title>
      <description>Enregistrement lundi 00h — {week_label}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{feed['audio_url']}?nocache={week_label}"
                 type="{feed['audio_type']}"
                 length="0"/>
      <guid isPermaLink="false">{guid}</guid>
      <itunes:duration>3600</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>

  </channel>
</rss>
"""

    path = f"feeds/{feed['filename']}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"✅ Generated {path} — guid: {guid}")

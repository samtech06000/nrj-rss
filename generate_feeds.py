#!/usr/bin/env python3
"""
Generate RSS podcast feeds for NRJ Paris and NRJ Belgique.
Each feed contains 168 episodes = 7 days × 24 hours.
Run daily at midnight Paris time via GitHub Actions.
Each episode guid includes the ISO week number so Apple Podcasts
picks up a fresh episode every week for that slot.
"""

from datetime import datetime, timezone, timedelta
import os

PARIS_TZ = timezone(timedelta(hours=1))
now = datetime.now(PARIS_TZ)

# ISO week number — changes every Monday, forces refresh in podcast apps
iso_year, iso_week, _ = now.isocalendar()
week_label = f"{iso_year}-W{iso_week:02d}"

GITHUB_USER = "YOUR_GITHUB_USERNAME"
GITHUB_REPO = "nrj-rss"
BASE_URL = f"https://{GITHUB_USER}.github.io/{GITHUB_REPO}"

DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Monday of the current ISO week (used for pubDate of each episode)
monday_this_week = now - timedelta(days=now.weekday())
monday_this_week = monday_this_week.replace(hour=0, minute=0, second=0, microsecond=0)

feeds = [
    {
        "filename": "nrj-paris.xml",
        "title": "NRJ Paris",
        "description": "Enregistrements NRJ Paris — toute la semaine, heure par heure",
        "image": f"{BASE_URL}/nrj-paris-logo.png",
        "base_url": "https://piges.alexandremartinat.com/NRJ_Paris",
        "ext": "mp3",
        "audio_type": "audio/mpeg",
        "guid_prefix": "nrj-paris",
    },
    {
        "filename": "nrj-belgique.xml",
        "title": "NRJ Belgique",
        "description": "Enregistrements NRJ Belgique — toute la semaine, heure par heure",
        "image": f"{BASE_URL}/nrj-belgique-logo.png",
        "base_url": "https://piges.alexandremartinat.com/NRJ_Belgique",
        "ext": "aac",
        "audio_type": "audio/aac",
        "guid_prefix": "nrj-belgique",
    },
]

os.makedirs("feeds", exist_ok=True)

for feed in feeds:
    items = []

    # Build 168 items: iterate days 0..6 (Mon..Sun), hours 0..23
    # Most recent first (Sunday 23h → Monday 00h)
    for day_idx in reversed(range(7)):
        for hour in reversed(range(24)):
            day_en = DAYS_EN[day_idx]
            day_fr = DAYS_FR[day_idx]

            # Compute actual datetime of this slot for pubDate
            slot_dt = monday_this_week + timedelta(days=day_idx, hours=hour)
            pub_date = slot_dt.strftime("%a, %d %b %Y %H:%M:%S +0100")

            audio_url = f"{feed['base_url']}/{day_en}/{hour:02d}.{feed['ext']}?w={week_label}"
            guid = f"{feed['guid_prefix']}-{week_label}-{day_en}-{hour:02d}"
            title = f"{feed['title']} — {day_fr} {hour:02d}h"

            items.append(f"""    <item>
      <title>{title}</title>
      <description>Semaine {week_label} — {day_fr} {hour:02d}h00</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}"
                 type="{feed['audio_type']}"
                 length="0"/>
      <guid isPermaLink="false">{guid}</guid>
      <itunes:duration>3600</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    last_build = now.strftime("%a, %d %b %Y %H:%M:%S +0100")
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
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{feed_url}" rel="self" type="application/rss+xml"/>
    <itunes:author>NRJ</itunes:author>
    <itunes:image href="{feed['image']}"/>
    <itunes:category text="Music"/>
    <itunes:explicit>false</itunes:explicit>

{chr(10).join(items)}

  </channel>
</rss>
"""

    path = f"feeds/{feed['filename']}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"✅ Generated {path} — {len(items)} episodes — week {week_label}")

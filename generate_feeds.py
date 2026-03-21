#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
import os

PARIS_TZ = timezone(timedelta(hours=1))
now = datetime.now(PARIS_TZ)

iso_year, iso_week, _ = now.isocalendar()
week_label = str(iso_year) + "-W" + str(iso_week).zfill(2)

GITHUB_USER = "samtech06000"
GITHUB_REPO = "nrj-rss"
BASE_URL = "https://" + GITHUB_USER + ".github.io/" + GITHUB_REPO

DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

monday_this_week = now - timedelta(days=now.weekday())
monday_this_week = monday_this_week.replace(hour=0, minute=0, second=0, microsecond=0)

feeds = [
    {
        "filename": "nrjparis.xml",
        "title": "NRJ Paris",
        "description": "Enregistrements NRJ Paris - toute la semaine, heure par heure",
        "image": BASE_URL + "/nrj-paris-logo.png",
        "base_url": "https://piges.alexandremartinat.com/NRJ_Paris",
        "ext": "mp3",
        "audio_type": "audio/mpeg",
        "guid_prefix": "nrj-paris",
    },
    {
        "filename": "nrj-belgique.xml",
        "title": "NRJ Belgique",
        "description": "Enregistrements NRJ Belgique - toute la semaine, heure par heure",
        "image": BASE_URL + "/nrj-belgique-logo.png",
        "base_url": "https://piges.alexandremartinat.com/NRJ_Belgique",
        "ext": "aac",
        "audio_type": "audio/aac",
        "guid_prefix": "nrj-belgique",
    },
]

os.makedirs("feeds", exist_ok=True)

for feed in feeds:
    items = []

    for day_idx in reversed(range(7)):
        for hour in reversed(range(24)):
            day_en = DAYS_EN[day_idx]
            day_fr = DAYS_FR[day_idx]

            slot_dt = monday_this_week + timedelta(days=day_idx, hours=hour)
            pub_date = slot_dt.strftime("%a, %d %b %Y %H:%M:%S +0100")

            audio_url = feed["base_url"] + "/" + day_en + "/" + str(hour).zfill(2) + "." + feed["ext"] + "?w=" + week_label
            guid = feed["guid_prefix"] + "-" + week_label + "-" + day_en + "-" + str(hour).zfill(2)
            title = feed["title"] + " - " + day_fr + " " + str(hour).zfill(2) + "h"

            item = "    <item>\n"
            item += "      <title>" + title + "</title>\n"
            item += "      <description>Semaine " + week_label + " - " + day_fr + " " + str(hour).zfill(2) + "h00</description>\n"
            item += "      <pubDate>" + pub_date + "</pubDate>\n"
            item += "      <enclosure url=\"" + audio_url + "\" type=\"" + feed["audio_type"] + "\" length=\"0\"/>\n"
            item += "      <guid isPermaLink=\"false\">" + guid + "</guid>\n"
            item += "      <itunes:duration>3600</itunes:duration>\n"
            item += "      <itunes:explicit>false</itunes:explicit>\n"
            item += "    </item>"
            items.append(item)

    last_build = now.strftime("%a, %d %b %Y %H:%M:%S +0100")
    feed_url = BASE_URL + "/feeds/" + feed["filename"]

    xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    xml += "<rss version=\"2.0\"\n"
    xml += "  xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\"\n"
    xml += "  xmlns:atom=\"http://www.w3.org/2005/Atom\">\n"
    xml += "  <channel>\n"
    xml += "    <title>" + feed["title"] + "</title>\n"
    xml += "    <link>" + BASE_URL + "</link>\n"
    xml += "    <description>" + feed["description"] + "</description>\n"
    xml += "    <language>fr</language>\n"
    xml += "    <lastBuildDate>" + last_build + "</lastBuildDate>\n"
    xml += "    <atom:link href=\"" + feed_url + "\" rel=\"self\" type=\"application/rss+xml\"/>\n"
    xml += "    <itunes:author>NRJ</itunes:author>\n"
    xml += "    <itunes:image href=\"" + feed["image"] + "\"/>\n"
    xml += "    <itunes:category text=\"Music\"/>\n"
    xml += "    <itunes:explicit>false</itunes:explicit>\n\n"
    xml += "\n".join(items)
    xml += "\n\n  </channel>\n</rss>\n"

    path = "feeds/" + feed["filename"]
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("Generated " + path + " - " + str(len(items)) + " episodes - week " + week_label)

# NRJ RSS Feeds

Flux RSS podcast auto-générés pour NRJ Paris et NRJ Belgique.  
Mis à jour chaque lundi à minuit via GitHub Actions → GitHub Pages.


### 1. URLs des flux RSS

```
https://samtech06000.github.io/nrj-rss/feeds/nrjparis.xml
https://samtech06000.github.io/nrj-rss/feeds/nrj-belgique.xml
```

Coller ces URLs dans Apple Podcasts → Bibliothèque → Ajouter un podcast par URL.

---

## Fonctionnement

- **Chaque lundi à 00h05 (heure de Paris)**, GitHub Actions tourne automatiquement
- Le script génère un nouveau `guid` basé sur le numéro de semaine (`2026-W12` etc.)
- Apple Podcasts détecte le nouveau guid et télécharge le nouvel épisode
- L'ancienne entrée est remplacée dans le flux (1 seul épisode à la fois)

## Forcer une mise à jour manuelle

Repo → **Actions** → `Generate & Deploy RSS Feeds` → **Run workflow**

# NRJ RSS Feeds

Flux RSS podcast auto-générés pour NRJ Paris et NRJ Belgique.  
Mis à jour chaque lundi à minuit via GitHub Actions → GitHub Pages.

## Setup (5 minutes)

### 1. Crée le repo GitHub

- Va sur [github.com/new](https://github.com/new)
- Nom : `nrj-rss`
- Visibilité : **Public** (requis pour GitHub Pages gratuit)
- Ne coche rien d'autre

### 2. Upload les fichiers

Dans le repo créé, uploade tous ces fichiers en conservant la structure :

```
nrj-rss/
├── generate_feeds.py
├── index.html
├── README.md
└── .github/
    └── workflows/
        └── update-feeds.yml
```

### 3. Mets ton username dans le script

Dans `generate_feeds.py`, ligne 18 :

```python
GITHUB_USER = "TON_USERNAME_GITHUB"
```

Remplace `YOUR_GITHUB_USERNAME` par ton vrai username GitHub.

### 4. Active GitHub Pages

- Repo → **Settings** → **Pages**
- Source : `Deploy from a branch`
- Branch : `main` / `root`
- Sauvegarde

### 5. Génère les feeds une première fois

- Repo → **Actions** → `Generate & Deploy RSS Feeds`
- Clique **Run workflow** → **Run workflow**

Les fichiers `feeds/nrj-paris.xml` et `feeds/nrj-belgique.xml` apparaissent dans le repo.

### 6. Tes URLs de flux RSS

```
https://TON_USERNAME.github.io/nrj-rss/feeds/nrj-paris.xml
https://TON_USERNAME.github.io/nrj-rss/feeds/nrj-belgique.xml
```

Colle ces URLs dans Apple Podcasts → Bibliothèque → Ajouter un podcast par URL.

---

## Fonctionnement

- **Chaque lundi à 00h05 (heure de Paris)**, GitHub Actions tourne automatiquement
- Le script génère un nouveau `guid` basé sur le numéro de semaine (`2026-W12` etc.)
- Apple Podcasts détecte le nouveau guid et télécharge le nouvel épisode
- L'ancienne entrée est remplacée dans le flux (1 seul épisode à la fois)

## Forcer une mise à jour manuelle

Repo → **Actions** → `Generate & Deploy RSS Feeds` → **Run workflow**

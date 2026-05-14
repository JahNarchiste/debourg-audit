# Debourg Audit — Guide du système de build

## Structure du projet

```
debourg-audit.fr/          ← racine GitHub Pages (ce que voit le visiteur)
│
├── index.html             ← généré automatiquement
├── css/style.css
├── js/main.js
├── assets/
│
├── pages/                 ← généré automatiquement
│   ├── approche.html
│   ├── offres.html
│   ├── pourquoi-nous.html
│   ├── articles/          ← articles de blog (généré)
│   └── ...
│
└── _build/                ← dossier de travail (ne pas uploader sur GitHub)
    ├── build.py           ← script de compilation
    ├── _includes/         ← éléments partagés (UNE seule source)
    │   ├── nav.html       ← navigation complète
    │   ├── footer.html    ← footer complet
    │   └── nav-css.html   ← CSS nav et dropdown
    └── _src/              ← sources des pages (NE PAS modifier les fichiers racine)
        ├── index.html
        └── pages/
            ├── approche.html
            ├── articles/
            │   └── mon-article.html
            └── ...
```

---

## Comment modifier la navigation ou le footer

1. Ouvrir `_includes/nav.html` ou `_includes/footer.html`
2. Faire la modification
3. Lancer `python build.py` depuis le dossier `_build/`
4. Tous les fichiers HTML sont régénérés automatiquement
5. Uploader les fichiers modifiés sur GitHub

---

## Comment modifier une page existante

1. Ouvrir le fichier correspondant dans `_src/pages/`
   - ex : `_src/pages/approche.html`
2. Faire la modification
3. Lancer `python build.py approche` (pour ne compiler que cette page)
   ou `python build.py` (pour tout recompiler)
4. Uploader le fichier modifié sur GitHub

---

## Créer un nouvel article

1. Copier `_src/pages/articles/article-template.html`
2. Renommer le fichier : ex `rge-en-5-mois.html`
3. Remplir les zones marquées ZONE 1, 2, 3
4. Lancer `python build.py rge-en-5-mois`
5. Uploader `pages/articles/rge-en-5-mois.html` sur GitHub

---

## Balises disponibles dans les sources

| Balise | Remplacé par |
|--------|-------------|
| `{{INCLUDE:nav.html}}` | Contenu de `_includes/nav.html` |
| `{{INCLUDE:footer.html}}` | Contenu de `_includes/footer.html` |
| `{{INCLUDE:nav-css.html}}` | CSS nav/dropdown |
| `{{ROOT}}` | Chemin vers la racine (`""` pour index, `"../"` pour pages/) |
| `{{PAGES}}` | Chemin vers pages/ (`"pages/"` pour index, `""` pour pages/) |

---

## Commandes rapides

```bash
# Tout recompiler
python build.py

# Compiler une seule page (filtre par nom de fichier)
python build.py approche
python build.py pourquoi-nous
python build.py mon-article

# Vérifier la structure
python build.py --list  # (à venir)
```

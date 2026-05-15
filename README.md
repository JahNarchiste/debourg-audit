# Debourg Audit — Site internet

Cabinet de conseil en efficacité opérationnelle pour PME, artisans et franchises.
Accompagnement à la création de société, agrément SAP, certification RGE, accompagnement dirigeant.

🌐 **Site en ligne :** [debourg-audit.fr](https://debourg-audit.fr)

---

## Présentation du projet

Site statique HTML/CSS/JS déployé via GitHub Pages. Pas de CMS, pas de framework — du HTML pur compilé par un script Python maison (`build.py`).

Le site propose :
- Des pages de services (audit, accompagnement dirigeant, SAP, RGE, certification)
- Une section "Nos dossiers" avec des articles de fond à destination des dirigeants et artisans
- Une newsletter Brevo intégrée

---

## Structure des dossiers

```
debourg-audit/
│
├── index.html                  ← page d'accueil
├── sitemap.xml                 ← sitemap (mis à jour automatiquement par build.py)
├── robots.txt
│
├── css/
│   └── style.css               ← feuille de style principale
│
├── js/
│   └── main.js                 ← scripts JS (menu mobile, interactions)
│
├── assets/                     ← images, logo, favicon
│
├── pages/                      ← toutes les pages du site
│   ├── offres.html
│   ├── approche.html
│   ├── accompagnement-dirigeant.html
│   ├── sap.html
│   ├── rge.html
│   ├── certification.html
│   ├── coordination-administrative.html
│   ├── parcours-ambition.html
│   ├── pourquoi-nous.html
│   ├── nos-dossiers.html
│   ├── contact.html
│   ├── mentions-legales.html
│   └── articles/               ← articles de blog (générés automatiquement)
│       └── compte-courant-associe.html
│
└── _build/                     ← dossier de travail LOCAL (ne pas uploader sur GitHub)
    ├── build.py                ← script de compilation
    ├── _includes/              ← éléments partagés (nav, footer)
    │   ├── nav.html
    │   ├── footer.html
    │   └── nav-css.html
    └── _src/                   ← sources des articles uniquement
        └── pages/
            └── articles/
                └── compte-courant-associe.html
```

> ⚠️ Le dossier `_build/` est un outil de travail local. Il ne doit **pas** être uploadé sur GitHub.

---

## Ce que fait le script build.py

Lancer `python build.py` depuis le dossier `_build/` effectue automatiquement :

1. **Mise à jour du dropdown** "Nos dossiers" dans `_includes/nav.html` avec les nouveaux articles
2. **Ajout de la carte** du nouvel article dans `pages/nos-dossiers.html`
3. **Compilation** de l'article source vers `pages/articles/`
4. **Injection du nav mis à jour** dans toutes les pages du site (`index.html`, `pages/*.html`, `pages/articles/*.html`)
5. **Mise à jour de `sitemap.xml`** avec l'URL du nouvel article

---

## Publier un nouvel article

### Étape 1 — Créer le fichier source

Créer un fichier HTML dans `_build/_src/pages/articles/` en respectant :
- Nommage : `nom-de-larticle.html` (minuscules, tirets, sans accents)
- Le bloc `ARTICLE_META` obligatoire en tête du fichier (voir ci-dessous)
- Les balises `{{ROOT}}`, `{{PAGES}}`, `{{INCLUDE:...}}`

**Bloc ARTICLE_META (à placer immédiatement après `<head>`) :**
```html
<!--
ARTICLE_META
titre: Titre complet de l'article
categorie: Gestion & Fiscalité
description: Description courte de 2-3 phrases affichée sur la carte nos-dossiers.
tags: Tag1, Tag2, Tag3
emoji: 💼
nav_label: Label court pour le dropdown
date: 14 mai 2025
date_sort: 2025-05-14
-->
```

**Catégories disponibles :**
- Parcours administratif
- Certification
- Gestion & Fiscalité
- Stratégie & Développement
- Juridique

### Étape 2 — Lancer le script

Ouvrir `cmd` dans le dossier `_build/` et lancer :
```cmd
python build.py
```

### Étape 3 — Uploader sur GitHub

Fichiers à uploader après chaque nouvel article :
- `pages/articles/NOM-DE-LARTICLE.html` ← nouvel article compilé
- `pages/nos-dossiers.html` ← carte ajoutée automatiquement
- `index.html` + tous les fichiers `pages/*.html` ← dropdown mis à jour
- `sitemap.xml` ← URL ajoutée automatiquement
- `_build/_includes/nav.html` ← lien ajouté automatiquement

---

## Modifier une page existante

Les pages du site (`pages/*.html`, `index.html`) sont modifiées **directement** — pas via `_src/`.

Après modification manuelle d'une page :
1. Uploader le fichier modifié sur GitHub
2. Si la modification concerne la nav ou le footer : modifier `_includes/nav.html` ou `_includes/footer.html` puis lancer `python build.py` pour propager sur toutes les pages

---

## Modifier la navigation ou le footer

1. Ouvrir `_build/_includes/nav.html` ou `_build/_includes/footer.html`
2. Faire la modification
3. Lancer `python build.py`
4. Uploader tous les fichiers HTML modifiés sur GitHub

---

## Balises disponibles dans les fichiers sources

| Balise | Remplacée par |
|--------|---------------|
| `{{INCLUDE:nav.html}}` | Contenu de `_includes/nav.html` |
| `{{INCLUDE:footer.html}}` | Contenu de `_includes/footer.html` |
| `{{INCLUDE:nav-css.html}}` | CSS nav et dropdown |
| `{{ROOT}}` | `../../` depuis articles/, `../` depuis pages/, `` depuis racine |
| `{{PAGES}}` | `../` depuis articles/, `` depuis pages/, `pages/` depuis racine |

---

## Sitemap

Le fichier `sitemap.xml` doit contenir le marqueur suivant pour que `build.py` puisse y insérer automatiquement les nouveaux articles :

```xml
  <!-- Articles — générés automatiquement par build.py -->
  <!-- FIN ARTICLES -->
```

Ce marqueur est placé juste avant `</urlset>`.

---

## Déploiement GitHub Pages

Le site est déployé automatiquement via GitHub Pages à chaque push sur la branche `main`.

**En cas de déploiement ignoré (Skipped) :**
- Vérifier que le push a bien été fait sur la branche `main`
- Vérifier dans GitHub → Settings → Pages que la source est bien `main` / `/ (root)`
- Vérifier dans GitHub → Actions que le workflow ne contient pas d'erreur

---

## Roadmap des articles

Voir le fichier `ROADMAP-articles.md` pour la liste des articles planifiés et leur statut.

---

## Technologies

- HTML5 / CSS3 / JavaScript vanilla
- Python 3 (script build.py local uniquement)
- GitHub Pages (hébergement)
- Brevo (newsletter)
- Google reCAPTCHA v3

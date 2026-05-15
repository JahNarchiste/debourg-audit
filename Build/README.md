# Guide de création d'un article — Debourg Audit

Ce document est destiné à la fois à un LLM (Claude) pour générer l'article en HTML et à l'utilisateur pour l'uploader sur le site.

---

## 1. Processus complet en 4 étapes

1. Définir le sujet et valider le contenu avec l'utilisateur
2. Générer le fichier HTML source (voir section 3)
3. Placer le fichier dans `_build/_src/pages/articles/`
4. Lancer `python build.py` depuis le dossier `_build/`

Le script fait automatiquement :
- Ajout du lien dans le dropdown "Nos dossiers" de toutes les pages du site
- Ajout de la carte dans `pages/nos-dossiers.html`
- Compilation de l'article vers `pages/articles/`
- Injection du nav mis à jour dans toutes les pages
- Mise à jour de `sitemap.xml`

---

## 2. Nommage du fichier

- Format : `nom-de-l-article.html` (minuscules, tirets, sans accents)
- Exemple : `compte-courant-associe.html`, `creer-sas-creuse.html`
- Placé dans : `_build/_src/pages/articles/`

---

## 3. Structure du fichier HTML source

### 3.1 Bloc métadonnées ARTICLE_META (obligatoire)

À placer **immédiatement après** `<head>`, avant toute autre balise :

```html
<!--
ARTICLE_META
titre: Titre complet de l'article (affiché sur la carte nos-dossiers)
categorie: Catégorie (voir liste ci-dessous)
description: Description courte de 2-3 phrases (affichée sur la carte nos-dossiers)
tags: Tag1, Tag2, Tag3 (affichés sur la carte nos-dossiers)
emoji: 💼 (affiché sur la carte nos-dossiers)
nav_label: Label court pour le dropdown de navigation (max 4-5 mots)
date: 14 mai 2025 (affiché sur la carte nos-dossiers)
date_sort: 2025-05-14 (format YYYY-MM-DD, utilisé pour trier les articles du plus récent au plus ancien)
-->
```

**Catégories disponibles :**
- Parcours administratif
- Certification
- Gestion & Fiscalité
- Stratégie & Développement
- Juridique

### 3.2 Balises de chemin (obligatoires)

Le fichier source utilise des balises que le script remplace automatiquement à la compilation :

| Balise | Remplacée par |
|--------|---------------|
| `{{ROOT}}` | `../../` (chemin vers la racine depuis articles/) |
| `{{PAGES}}` | `../` (chemin vers pages/ depuis articles/) |
| `{{INCLUDE:nav.html}}` | Contenu de `_includes/nav.html` |
| `{{INCLUDE:footer.html}}` | Contenu de `_includes/footer.html` |
| `{{INCLUDE:nav-css.html}}` | Contenu de `_includes/nav-css.html` |

À utiliser dans les liens et imports :
```html
<link rel="stylesheet" href="{{ROOT}}css/style.css" />
<link rel="icon" href="{{ROOT}}assets/favicon.png" type="image/png" />
<a href="{{PAGES}}contact.html">Contact</a>
<a href="{{PAGES}}accompagnement-dirigeant.html">Accompagnement</a>
```

### 3.3 Structure HTML complète

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<!--
ARTICLE_META
titre: ...
categorie: ...
description: ...
tags: ...
emoji: ...
nav_label: ...
date: ...
date_sort: YYYY-MM-DD
-->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="[Description SEO 150 caractères max]" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://debourg-audit.fr/pages/articles/NOM-DU-FICHIER.html" />
  <meta property="og:title" content="[Titre SEO] — Debourg Audit" />
  <meta property="og:description" content="[Description SEO]" />
  <meta property="og:image" content="https://debourg-audit.fr/assets/logo_transparent.png" />
  <meta property="og:locale" content="fr_FR" />
  <meta property="og:site_name" content="Debourg Audit" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="[Titre SEO] — Debourg Audit" />
  <meta name="twitter:description" content="[Description SEO]" />
  <link rel="canonical" href="https://debourg-audit.fr/pages/articles/NOM-DU-FICHIER.html" />
  <title>[Titre SEO complet] — Debourg Audit</title>

  <!-- JSON-LD Article -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "[Titre de l'article]",
    "description": "[Description courte]",
    "author": {"@type": "Person", "name": "Antonin Debourg"},
    "publisher": {"@type": "Organization", "name": "Debourg Audit", "url": "https://debourg-audit.fr"},
    "datePublished": "YYYY-MM-DD",
    "url": "https://debourg-audit.fr/pages/articles/NOM-DU-FICHIER.html",
    "mainEntityOfPage": "https://debourg-audit.fr/pages/articles/NOM-DU-FICHIER.html"
  }
  </script>

  <link rel="stylesheet" href="{{ROOT}}css/style.css" />
  <link rel="icon" href="{{ROOT}}assets/favicon.png" type="image/png" />
  {{INCLUDE:nav-css.html}}

  <!-- Styles spécifiques à l'article — voir section 4 -->
  <style>
    /* ... */
  </style>

  <script src="https://www.google.com/recaptcha/api.js?render=6LdlDtwsAAAAAFpFJrTwKEAXuAr2u-Jf5b-0gP12"></script>
</head>
<body>

{{INCLUDE:nav.html}}

<div style="padding-top: 80px;">
<div class="article-wrap">

  <header class="article-header">
    <div class="article-header__categorie">CATÉGORIE</div>
    <h1 class="article-header__titre">TITRE DE L'ARTICLE</h1>
    <p class="article-header__intro">INTRODUCTION (2-3 phrases)</p>
    <div class="article-header__meta">
      <span>📅 JJ mois AAAA</span>
      <span>⏱ XX min de lecture</span>
    </div>
  </header>

  <article class="article-body">

    <!-- CONTENU DE L'ARTICLE — voir section 5 -->

    <!-- CTA Contact -->
    <!-- CTA Newsletter -->
    <!-- Navigation retour -->

  </article>
</div>
</div>

{{INCLUDE:footer.html}}

<!-- Scripts Brevo + reCAPTCHA — voir section 6 -->

</body>
</html>
```

---

## 4. CSS spécifique à l'article

Copier ce bloc `<style>` dans le `<head>` de chaque article (identique pour tous les articles) :

```html
<style>
  .article-wrap { max-width:760px; margin:0 auto; padding:0 24px; }
  .article-header { padding:48px 0 40px; border-bottom:1px solid var(--gris-200); margin-bottom:48px; }
  .article-header__categorie { font-size:0.78rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:var(--cuivre); margin-bottom:16px; }
  .article-header__titre { font-family:var(--font-titre); font-size:clamp(1.8rem,4vw,2.8rem); font-weight:700; color:var(--bleu); line-height:1.2; margin-bottom:20px; }
  .article-header__intro { font-size:1.1rem; color:var(--gris-500); line-height:1.75; margin-bottom:24px; }
  .article-header__meta { display:flex; align-items:center; gap:20px; font-size:0.85rem; color:var(--gris-500); }
  .article-header__meta span { display:flex; align-items:center; gap:6px; }
  .article-body { padding-bottom:64px; }
  .article-body h2 { font-family:var(--font-titre); font-size:1.7rem; font-weight:700; color:var(--bleu); margin:48px 0 16px; line-height:1.25; }
  .article-body h3 { font-family:var(--font-titre); font-size:1.25rem; font-weight:700; color:var(--bleu); margin:32px 0 12px; }
  .article-body p { font-size:1rem; color:var(--gris-800); line-height:1.85; margin-bottom:20px; }
  .article-body ul, .article-body ol { margin:0 0 20px 24px; }
  .article-body ul { list-style:disc; }
  .article-body ol { list-style:decimal; }
  .article-body li { font-size:1rem; color:var(--gris-800); line-height:1.75; margin-bottom:8px; }
  .article-body strong { color:var(--bleu); font-weight:600; }
  .article-body a { color:var(--cuivre); text-decoration:underline; }
  .article-body a:hover { color:var(--bleu); }
  .article-body hr { border:none; border-top:1px solid var(--gris-200); margin:40px 0; }
  .article-body blockquote { border-left:3px solid var(--cuivre); margin:32px 0; padding:4px 0 4px 24px; font-family:var(--font-titre); font-size:1.3rem; font-style:italic; color:var(--bleu); line-height:1.5; }
  .article-body .encadre { background:var(--gris-100); border-left:4px solid var(--cuivre); border-radius:0 8px 8px 0; padding:20px 24px; margin:28px 0; }
  .article-body .encadre p { margin-bottom:0; }
  .article-body .encadre p + p { margin-top:10px; }
  .article-body .alerte { background:rgba(192,122,69,0.08); border:1px solid rgba(192,122,69,0.25); border-radius:8px; padding:18px 22px; margin:28px 0; font-size:0.9rem; }
  .article-cta { background:var(--bleu); border-radius:14px; padding:40px; text-align:center; margin:48px 0; }
  .article-cta__titre { font-family:var(--font-titre); font-size:1.5rem; font-weight:700; color:var(--blanc); margin-bottom:10px; }
  .article-cta__titre em { color:var(--cuivre); font-style:normal; }
  .article-nav { display:flex; justify-content:space-between; align-items:center; padding:32px 0; border-top:1px solid var(--gris-200); gap:16px; }
  .article-nav__retour { display:inline-flex; align-items:center; gap:8px; font-size:0.875rem; font-weight:600; color:var(--gris-500); text-decoration:none; transition:color 0.2s; }
  .article-nav__retour:hover { color:var(--bleu); }
  .article-nav__retour svg { width:16px; height:16px; }
  /* Tableau de simulation */
  .simulation-table { width:100%; border-collapse:collapse; margin:28px 0; font-size:0.9rem; }
  .simulation-table th { background:var(--bleu); color:var(--blanc); padding:12px 16px; text-align:left; font-family:var(--font-titre); font-weight:600; }
  .simulation-table td { padding:12px 16px; border-bottom:1px solid rgba(26,54,93,0.08); color:var(--gris-800); }
  .simulation-table tr:nth-child(even) td { background:var(--gris-100); }
  .simulation-table tr:last-child td { border-bottom:none; }
  .simulation-table td:first-child { font-weight:600; color:var(--bleu); }
</style>
```

---

## 5. Éléments de contenu disponibles

### Paragraphe simple
```html
<p>Texte du paragraphe.</p>
```

### Titre de section
```html
<h2>Titre H2</h2>
<h3>Titre H3</h3>
```

### Encadré (fond gris, bordure cuivre)
```html
<div class="encadre">
  <p><strong>À retenir :</strong> Texte de l'encadré.</p>
</div>
```

### Alerte / mise en garde
```html
<div class="alerte">
  <p>⚠️ <strong>Attention :</strong> Texte de l'alerte.</p>
</div>
```

### Citation / blockquote
```html
<blockquote>
  Phrase mise en valeur.
</blockquote>
```

### Liste à puces
```html
<ul>
  <li>Élément 1</li>
  <li>Élément 2</li>
</ul>
```

### Tableau de simulation
```html
<table class="simulation-table">
  <thead>
    <tr>
      <th>Colonne 1</th>
      <th>Colonne 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Valeur</td>
      <td>Valeur</td>
    </tr>
  </tbody>
</table>
```

### Séparateur horizontal
```html
<hr>
```

---

## 6. Blocs CTA (à copier tels quels en fin d'article)

### CTA Contact
```html
<div class="article-cta">
  <div class="article-cta__titre">Titre du CTA<br/><em>sous-titre en cuivre</em></div>
  <p style="font-size:0.9rem; color:rgba(255,255,255,0.85); margin-bottom:24px;">Texte descriptif du CTA.</p>
  <a href="{{PAGES}}contact.html" style="display:inline-flex; align-items:center; gap:8px; margin-top:8px; padding:13px 28px; background:#C07A45; color:#fff; border:none; border-radius:8px; font-weight:700; font-size:0.9rem; text-decoration:none; font-family:var(--font-corps,'DM Sans',sans-serif); transition:background 0.2s;">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
    Prendre contact
  </a>
</div>
```

### CTA Newsletter Brevo (copier tel quel — ne pas modifier)
```html
<div class="article-cta">
  <div class="article-cta__titre">Recevoir les prochains dossiers<br/><em>directement dans votre boîte mail</em></div>
  <p style="font-size:0.9rem; color:rgba(255,255,255,0.85); margin-bottom:24px;">Un dossier à la fois, quand il est prêt. Pas de spam.</p>
  <link rel="stylesheet" href="https://sibforms.com/forms/end-form/build/sib-styles.css">
  <style>
    #sib-form .sib-form-block:first-child p { display:none; }
    #sib-form .sib-form-block:nth-child(2) { display:none; }
    #sib-form .entry__label { font-size:0.8rem !important; font-weight:600 !important; color:rgba(255,255,255,0.75) !important; letter-spacing:0.06em !important; text-transform:uppercase !important; font-family:var(--font-corps,'DM Sans',sans-serif) !important; margin-bottom:8px !important; }
    #sib-form .entry__specification { display:none !important; }
    #sib-form #EMAIL { width:100% !important; padding:16px 20px !important; border:2px solid rgba(255,255,255,0.25) !important; border-radius:10px !important; background:rgba(255,255,255,0.12) !important; color:#1a1a1a !important; font-size:1rem !important; font-family:var(--font-corps,'DM Sans',sans-serif) !important; box-sizing:border-box !important; outline:none !important; transition:border-color 0.2s !important; }
    #sib-form #EMAIL::placeholder { color:rgba(255,255,255,0.5) !important; }
    #sib-form #EMAIL:focus { border-color:#C07A45 !important; }
    #sib-form .sib-form-block__button { width:100% !important; padding:16px 24px !important; background:#C07A45 !important; color:#fff !important; border:none !important; border-radius:10px !important; font-size:1rem !important; font-weight:700 !important; font-family:var(--font-corps,'DM Sans',sans-serif) !important; cursor:pointer !important; letter-spacing:0.02em !important; margin-top:12px !important; transition:background 0.2s !important; }
    #sib-form .sib-form-block__button:hover { background:#a8662e !important; }
    #sib-form .entry__error { font-size:0.8rem !important; font-family:var(--font-corps,'DM Sans',sans-serif) !important; }
    #sib-form-container { padding:0 !important; }
    .sib-form { background:transparent !important; padding:0 !important; }
    #success-message .sib-form-message-panel__inner-text { color:#fff !important; font-family:var(--font-corps,'DM Sans',sans-serif) !important; }
    #error-message .sib-form-message-panel__inner-text { font-family:var(--font-corps,'DM Sans',sans-serif) !important; }
  </style>
  <div class="sib-form" style="max-width:420px; margin:0 auto;">
    <div id="sib-form-container" class="sib-form-container">
      <div id="error-message" class="sib-form-message-panel" style="display:none; font-size:14px; font-family:Helvetica,sans-serif; color:#661d1d; background-color:#ffeded; border-radius:3px; border-color:#ff4949;">
        <div class="sib-form-message-panel__text sib-form-message-panel__text--center">
          <span class="sib-form-message-panel__inner-text">Nous n&#039;avons pas pu confirmer votre inscription.</span>
        </div>
      </div>
      <div id="success-message" class="sib-form-message-panel" style="display:none; font-size:14px; font-family:Helvetica,sans-serif; color:#085229; background-color:#e7faf0; border-radius:3px; border-color:#13ce66;">
        <div class="sib-form-message-panel__text sib-form-message-panel__text--center">
          <span class="sib-form-message-panel__inner-text">Votre inscription est confirmée. ✅</span>
        </div>
      </div>
      <div id="sib-container" class="sib-container--large sib-container--vertical">
        <form id="sib-form" method="POST" action="https://c2d92939.sibforms.com/serve/MUIFALfqr-TsXCtGnIdK41K3z8WJl94uZnGHi6PE_SIwWbJ7CLtp4pAWBoEOmqPNShezT6IaNglt5dFeAl10aHDbZzcyiESJjK0UIfhqppvmSXmsi7qscgHlhmTueHLGtjUMviOooVC6CfsGweboknowKMeSvi3OeGweZcWphZdAaJXYZcIUjLC3bEKq8UYPjKI6YK3E5Ma8fl9dXQ==" data-type="subscription">
          <div class="sib-form-block" style="font-size:32px; font-weight:700; font-family:Helvetica,sans-serif; color:#3C4858; background-color:transparent; text-align:left;"><p>Newsletter</p></div>
          <div class="sib-form-block" style="font-size:16px; font-family:Helvetica,sans-serif; color:#3C4858; background-color:transparent; text-align:left;"><div class="sib-text-form-block"><p>Newsletter</p></div></div>
          <div class="sib-input sib-form-block">
            <div class="form__entry entry_block">
              <div class="form__label-row">
                <label class="entry__label" style="font-weight:700; font-size:16px; font-family:Helvetica,sans-serif; color:#3c4858;" for="EMAIL" data-required="*">Votre adresse email</label>
                <div class="entry__field">
                  <input class="input" type="text" id="EMAIL" name="EMAIL" autocomplete="off" placeholder="vous@exemple.fr" data-required="true" required />
                </div>
              </div>
              <label class="entry__error entry__error--primary"></label>
            </div>
          </div>
          <div class="sib-form-block" style="text-align:left;">
            <button class="sib-form-block__button sib-form-block__button-with-loader" form="sib-form" type="submit">S'abonner</button>
          </div>
          <input type="text" name="email_address_check" value="" class="input--hidden">
          <input type="hidden" name="locale" value="fr">
        </form>
      </div>
    </div>
  </div>
  <p style="font-size:0.72rem; color:rgba(255,255,255,0.45); margin-top:12px;">Désinscription libre à tout moment. Données non transmises à des tiers.</p>
</div>
```

### Navigation retour
```html
<div class="article-nav">
  <a href="{{PAGES}}nos-dossiers.html" class="article-nav__retour">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M11 17l-5-5m0 0l5-5m-5 5h12"/></svg>
    Retour aux dossiers
  </a>
</div>
```

---

## 7. Scripts à placer avant `</body>` (copier tels quels)

```html
<script src="{{ROOT}}js/main.js"></script>
<script>
  window.REQUIRED_CODE_ERROR_MESSAGE = 'Veuillez choisir un code pays';
  window.LOCALE = 'fr';
  window.EMAIL_INVALID_MESSAGE = "Les informations que vous avez fournies ne sont pas valides.";
  window.REQUIRED_ERROR_MESSAGE = "Vous devez renseigner ce champ.";
  window.GENERIC_INVALID_MESSAGE = "Les informations que vous avez fournies ne sont pas valides.";
  window.translation = { common: { selectedList: '{quantity} liste sélectionnée', selectedLists: '{quantity} listes sélectionnées', selectedOption: '{quantity} sélectionné', selectedOptions: '{quantity} sélectionnés' } };
  var AUTOHIDE = Boolean(0);
</script>
<script defer src="https://sibforms.com/forms/end-form/build/main.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var forms = document.querySelectorAll('#sib-form');
  forms.forEach(function(form) {
    if (!form.querySelector('input[name="g-recaptcha-response"]')) {
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'g-recaptcha-response';
      input.id = 'g-recaptcha-response';
      form.appendChild(input);
    }
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var f = this;
      grecaptcha.ready(function() {
        grecaptcha.execute('6LdlDtwsAAAAAFpFJrTwKEAXuAr2u-Jf5b-0gP12', {action: 'newsletter_subscribe'}).then(function(token) {
          f.querySelector('#g-recaptcha-response').value = token;
          f.removeEventListener('submit', arguments.callee);
          HTMLFormElement.prototype.submit.call(f);
        });
      });
    }, false);
  });
});
</script>
```

---

## 8. SEO — règles à respecter

- `<title>` : inclure les mots-clés principaux + "Creuse" si pertinent + "Debourg Audit" en fin
- `<meta name="description">` : 150 caractères max, inclure mots-clés cibles
- `<h1>` : un seul par page, reprend le titre principal
- `<h2>` / `<h3>` : structurent le contenu, doivent contenir des mots-clés naturellement
- Lien interne : toujours ajouter un lien vers la page de service correspondante (`accompagnement-dirigeant.html`, `sap.html`, `rge.html`, `certification.html`)
- JSON-LD `Article` : obligatoire, avec `datePublished` au format `YYYY-MM-DD`

---

## 9. Checklist avant de lancer build.py

- [ ] Fichier nommé en minuscules avec tirets, sans accents
- [ ] Bloc `ARTICLE_META` complet (tous les champs remplis)
- [ ] `date_sort` au format `YYYY-MM-DD`
- [ ] Balises `{{ROOT}}`, `{{PAGES}}`, `{{INCLUDE:...}}` présentes
- [ ] CTA Contact et CTA Newsletter présents
- [ ] Navigation retour présente
- [ ] Scripts Brevo + reCAPTCHA présents avant `</body>`
- [ ] Fichier placé dans `_build/_src/pages/articles/`
- [ ] `sitemap.xml` contient le marqueur `<!-- FIN ARTICLES -->`

---

## 10. Lancer le build

Depuis le dossier `_build/` dans l'invite de commandes Windows (`cmd`) :

```cmd
python build.py
```

Le script affiche les étapes et confirme chaque mise à jour. En cas d'erreur, le message indique le fichier et la ligne concernés.

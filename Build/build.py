#!/usr/bin/env python3
"""
Debourg Audit — Script de build
================================
Utilisation :
  python build.py   → fait tout automatiquement

Ce que fait le script :
  1. Lit les articles dans _src/pages/articles/
  2. Ajoute les nouveaux liens dans _includes/nav.html
  3. Ajoute les nouvelles cartes dans pages/nos-dossiers.html
  4. Recompile les articles depuis _src/pages/articles/ vers pages/articles/
  5. Réinjecte le nav mis à jour dans TOUTES les pages HTML de pages/ et index.html

Structure attendue :
  _build/
    build.py               <- ce script
    _includes/
      nav.html             <- navigation avec balises {{PAGES}} et {{ROOT}}
      footer.html          <- footer
      nav-css.html         <- CSS nav
    _src/
      pages/
        articles/          <- sources des articles (avec bloc ARTICLE_META)

  pages/                   <- dossier racine du site (modifie directement)
    nos-dossiers.html
    *.html
    articles/
  index.html

Metadonnees articles (bloc en commentaire en tete de chaque fichier source) :
  <!--
  ARTICLE_META
  titre: Titre de l'article
  categorie: Categorie
  description: Description courte
  tags: Tag1, Tag2, Tag3
  emoji: emoji
  nav_label: Label court pour le dropdown
  -->
"""

import os, re, sys

BASE         = os.path.dirname(os.path.abspath(__file__))
INCLUDES_DIR = os.path.join(BASE, '_includes')
SRC_ARTICLES = os.path.join(BASE, '_src', 'pages', 'articles')
OUT_ROOT     = os.path.dirname(BASE)
OUT_PAGES    = os.path.join(OUT_ROOT, 'pages')

NAV_MARKER      = '            <li><a href="{{PAGES}}nos-dossiers.html">Newsletter</a></li>'
DOSSIERS_MARKER = '<!-- \u2550\u2550\u2550 FIN DOSSIERS \u2014 coller les nouvelles cartes juste au-dessus \u2550\u2550\u2550 -->'


def load_include(name):
    path = os.path.join(INCLUDES_DIR, name)
    if not os.path.exists(path):
        print(f'  [!] Include manquant : {name}')
        return f'<!-- INCLUDE MANQUANT : {name} -->'
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def read_article_meta(src_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<!--\s*ARTICLE_META\s*(.*?)-->', content, re.DOTALL)
    if not match:
        return None
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if ':' in line:
            key, _, value = line.partition(':')
            meta[key.strip().lower()] = value.strip()
    return meta


def build_dossier_card(filename, meta):
    tags_html = '\n'.join(
        f'            <span class="dossier-card__tag">{t.strip()}</span>'
        for t in meta.get('tags', '').split(',') if t.strip()
    )
    slug = filename.upper().replace('.HTML', '')
    titre = meta.get('titre', '')
    categorie = meta.get('categorie', '')
    description = meta.get('description', '')
    emoji = meta.get('emoji', '')
    date = meta.get('date', '')
    date_html = f'\n          <div style="font-size:0.78rem; color:var(--gris-500); margin-bottom:8px;">📅 {date}</div>' if date else ''
    return (
        f'\n      <!-- DOSSIER {slug} \u2014 g\u00e9n\u00e9r\u00e9 automatiquement -->\n'
        f'      <a href="articles/{filename}" class="dossier-card">\n'
        f'        <div class="dossier-card__header">\n'
        f'          <div class="dossier-card__icon">{emoji}</div>\n'
        f'          <div class="dossier-card__meta">\n'
        f'            <div class="dossier-card__categorie">{categorie}</div>\n'
        f'            <div class="dossier-card__titre">{titre}</div>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'        <div class="dossier-card__body">{date_html}\n'
        f'          <div class="dossier-card__desc">{description}</div>\n'
        f'          <div class="dossier-card__tags">\n'
        f'{tags_html}\n'
        f'          </div>\n'
        f'          <div class="dossier-card__cta">\n'
        f'            Lire le dossier\n'
        f'            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </a>'
    )


def discover_articles():
    if not os.path.exists(SRC_ARTICLES):
        return []
    articles = []
    for fname in os.listdir(SRC_ARTICLES):
        if not fname.endswith('.html'):
            continue
        src_path = os.path.join(SRC_ARTICLES, fname)
        meta = read_article_meta(src_path)
        if meta:
            articles.append((fname, meta, src_path))
        else:
            print(f'  [!] Metadonnees ARTICLE_META manquantes : {fname}')
    # Tri par date_sort décroissant (plus récent en premier)
    articles.sort(key=lambda x: x[1].get('date_sort', '0000-00-00'), reverse=True)
    return articles


def compile_article(src_path, fname):
    out_path = os.path.join(OUT_PAGES, 'articles', fname)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()
    def replace_include(m):
        return load_include(m.group(1))
    content = re.sub(r'\{\{INCLUDE:([^}]+)\}\}', replace_include, content)
    content = content.replace('{{ROOT}}', '../../')
    content = content.replace('{{PAGES}}', '../')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  [OK] Article compile : {fname}')


def update_nav(articles):
    nav_path = os.path.join(INCLUDES_DIR, 'nav.html')
    if not os.path.exists(nav_path):
        print('  [!] _includes/nav.html introuvable.')
        return
    with open(nav_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if NAV_MARKER not in content:
        print('  [!] Marqueur Newsletter introuvable dans nav.html.')
        return

    # Supprimer tous les liens articles existants
    content = re.sub(r'\s*<li><a href="\{\{PAGES\}\}articles/[^"]+\.html">[^<]+</a></li>', '', content)

    # Réinsérer tous les liens triés par date_sort décroissant (déjà triés)
    new_links = []
    for fname, meta, _ in articles:
        label = meta.get('nav_label', fname)
        new_links.append(f'            <li><a href="{{{{PAGES}}}}articles/{fname}">{label}</a></li>')

    if new_links:
        insertion = '\n'.join(new_links) + '\n' + NAV_MARKER
        content = content.replace(NAV_MARKER, insertion, 1)

    with open(nav_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  [OK] {len(new_links)} lien(s) mis à jour dans nav.html (ordre chronologique inversé)')


def update_nos_dossiers(articles):
    path = os.path.join(OUT_PAGES, 'nos-dossiers.html')
    if not os.path.exists(path):
        print('  [!] pages/nos-dossiers.html introuvable.')
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Recherche du marqueur FIN DOSSIERS (souple)
    match = re.search(r'<!--[^\S\n]*.*?FIN DOSSIERS.*?-->', content)
    if not match:
        print('  [!] Marqueur FIN DOSSIERS introuvable.')
        return

    marker = match.group(0)

    # Supprimer toutes les cartes générées automatiquement existantes
    content = re.sub(r'\n\s*<!-- DOSSIER [A-Z0-9\-]+ — généré automatiquement -->.*?</a>', '', content, flags=re.DOTALL)

    # Réinsérer toutes les cartes triées par date_sort décroissant (déjà triées par discover_articles)
    all_cards = [build_dossier_card(fname, meta) for fname, meta, _ in articles]

    if all_cards:
        insertion = marker + '\n' + '\n'.join(all_cards)
        content = content.replace(marker, insertion)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'  [OK] {len(all_cards)} carte(s) insérée(s) dans nos-dossiers.html (ordre chronologique inversé)')


def update_sitemap(articles):
    """Ajoute les nouveaux articles dans sitemap.xml."""
    sitemap_path = os.path.join(OUT_ROOT, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        print('  [!] sitemap.xml introuvable.')
        return
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    marker = '<!-- FIN ARTICLES -->'
    if marker not in content:
        print('  [!] Marqueur FIN ARTICLES introuvable dans sitemap.xml.')
        return
    new_entries = []
    for fname, meta, _ in articles:
        url = f'https://debourg-audit.fr/pages/articles/{fname}'
        if url in content:
            print(f'  [=] Sitemap deja a jour : {fname}')
        else:
            date_sort = meta.get('date_sort', '2025-01-01')
            new_entries.append(
                f'  <url>\n'
                f'    <loc>{url}</loc>\n'
                f'    <lastmod>{date_sort}</lastmod>\n'
                f'    <changefreq>yearly</changefreq>\n'
                f'    <priority>0.7</priority>\n'
                f'  </url>'
            )
            print(f'  [+] Sitemap mis a jour : {fname}')
    if new_entries:
        insertion = '\n'.join(new_entries) + '\n  ' + marker
        content = content.replace(marker, insertion)
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(content)



def inject_nav_all_pages():
    nav_html    = load_include('nav.html')
    footer_html = load_include('footer.html')

    nav_pattern    = re.compile(r'<nav class="nav">.*?</nav>', re.DOTALL)
    footer_pattern = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)

    count = 0

    # index.html
    index_path = os.path.join(OUT_ROOT, 'index.html')
    if os.path.exists(index_path):
        nav_c    = nav_html.replace('{{ROOT}}', '').replace('{{PAGES}}', 'pages/')
        footer_c = footer_html.replace('{{ROOT}}', '').replace('{{PAGES}}', 'pages/')
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = nav_pattern.sub(nav_c, content)
        content = footer_pattern.sub(footer_c, content)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [~] index.html')
        count += 1

    # pages/*.html
    for fname in os.listdir(OUT_PAGES):
        if not fname.endswith('.html'):
            continue
        fpath    = os.path.join(OUT_PAGES, fname)
        nav_c    = nav_html.replace('{{ROOT}}', '../').replace('{{PAGES}}', '')
        footer_c = footer_html.replace('{{ROOT}}', '../').replace('{{PAGES}}', '')
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = nav_pattern.sub(nav_c, content)
        content = footer_pattern.sub(footer_c, content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [~] pages/{fname}')
        count += 1

    # pages/articles/*.html
    articles_dir = os.path.join(OUT_PAGES, 'articles')
    if os.path.exists(articles_dir):
        for fname in os.listdir(articles_dir):
            if not fname.endswith('.html'):
                continue
            fpath    = os.path.join(articles_dir, fname)
            nav_c    = nav_html.replace('{{ROOT}}', '../../').replace('{{PAGES}}', '../')
            footer_c = footer_html.replace('{{ROOT}}', '../../').replace('{{PAGES}}', '../')
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = nav_pattern.sub(nav_c, content)
            content = footer_pattern.sub(footer_c, content)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [~] pages/articles/{fname}')
            count += 1

    print(f'\n  {count} page(s) mises a jour.')


def main():
    articles = discover_articles()

    print('\n-- Etape 1 : nav.html --------------------------------')
    update_nav(articles)

    print('\n-- Etape 2 : nos-dossiers.html -----------------------')
    update_nos_dossiers(articles)

    print('\n-- Etape 2b : sitemap.xml ----------------------------')
    update_sitemap(articles)

    print('\n-- Etape 3 : compilation articles --------------------')
    for fname, meta, src_path in articles:
        compile_article(src_path, fname)

    print('\n-- Etape 4 : injection nav toutes les pages ----------')
    inject_nav_all_pages()

    print('\n[OK] Build termine.')


if __name__ == '__main__':
    main()

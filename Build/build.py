#!/usr/bin/env python3
"""
Debourg Audit — Script de build
================================
Utilisation :
  python build.py            → compile toutes les pages
  python build.py approche   → compile uniquement les pages contenant "approche"

Structure :
  _includes/nav.html         → navigation (une seule source)
  _includes/footer.html      → footer (une seule source)
  _includes/nav-css.html     → CSS nav/dropdown
  _src/pages/*.html          → sources des pages (pages/)
  _src/pages/articles/*.html → sources des articles
  _src/index.html            → source de l'accueil

  → Sortie dans le dossier racine (index.html) et pages/ (autres pages)

Balises disponibles dans les sources :
  {{INCLUDE:nom-du-fichier}}   → insère _includes/nom-du-fichier
  {{ROOT}}                     → chemin vers la racine (vide pour index, ../ pour pages/)
  {{PAGES}}                    → chemin vers pages/ (pages/ pour index, vide pour pages/)
"""

import os, re, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
INCLUDES_DIR = os.path.join(BASE, '_includes')
SRC_DIR = os.path.join(BASE, '_src')
OUT_ROOT = os.path.dirname(BASE)  # dossier parent = racine du site

# ── Lecture des includes ──────────────────────────────────────────────────────
def load_include(name):
    path = os.path.join(INCLUDES_DIR, name)
    if not os.path.exists(path):
        print(f'  ⚠️  Include manquant : {name}')
        return f'<!-- INCLUDE MANQUANT : {name} -->'
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# ── Compilation d'un fichier source ──────────────────────────────────────────
def compile_page(src_path, out_path, root_prefix, pages_prefix):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Injecter les includes
    def replace_include(m):
        return load_include(m.group(1))
    content = re.sub(r'\{\{INCLUDE:([^}]+)\}\}', replace_include, content)

    # Remplacer les préfixes de chemin
    content = content.replace('{{ROOT}}', root_prefix)
    content = content.replace('{{PAGES}}', pages_prefix)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)

# ── Découverte des sources ────────────────────────────────────────────────────
def discover_sources():
    sources = []
    for dirpath, _, files in os.walk(SRC_DIR):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            src_path = os.path.join(dirpath, fname)
            rel = os.path.relpath(src_path, SRC_DIR)  # ex: index.html ou pages/approche.html

            if rel == 'index.html':
                out_path = os.path.join(OUT_ROOT, 'index.html')
                root_prefix = ''
                pages_prefix = 'pages/'
            elif rel.startswith('pages' + os.sep + 'articles' + os.sep):
                # Articles : pages/articles/mon-article.html
                out_path = os.path.join(OUT_ROOT, rel)
                root_prefix = '../../'
                pages_prefix = '../'
            elif rel.startswith('pages' + os.sep):
                # Pages standard : pages/approche.html
                out_path = os.path.join(OUT_ROOT, rel)
                root_prefix = '../'
                pages_prefix = ''
            else:
                continue

            sources.append((src_path, out_path, root_prefix, pages_prefix, rel))
    return sources

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    filter_kw = sys.argv[1].lower() if len(sys.argv) > 1 else None
    sources = discover_sources()

    compiled = 0
    for src_path, out_path, root_prefix, pages_prefix, rel in sources:
        if filter_kw and filter_kw not in rel.lower():
            continue
        compile_page(src_path, out_path, root_prefix, pages_prefix)
        print(f'  ✅  {rel}  →  {os.path.relpath(out_path, OUT_ROOT)}')
        compiled += 1

    print(f'\n{compiled} page(s) compilée(s).')

if __name__ == '__main__':
    main()

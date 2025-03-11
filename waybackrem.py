#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  11-03-2025
Last update: 11-03-2025
Version: 1.0
Description: Remove a links to wayback machine  
Example of use: python remove_wayback.py /PATCH/TO/THE/LOCAL/SITE
'''

import os
import re
import sys
from bs4 import BeautifulSoup

def clean_html(html):
    # Remplacer les URL de type :
    # https://web.archive.org/web/<timestamp>/<url_origine>
    # par l'url d'origine
    pattern = re.compile(r'https?://web\.archive\.org/web/\d+/(https?://[^\s\'"]+)')
    return pattern.sub(r'\1', html)

def process_html_file(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath} : {e}")
        return

    # Nettoyer les URL Wayback Machine dans le code brut
    cleaned_html = clean_html(html)

    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(cleaned_html, 'html.parser')

    # Fonction d'accès sécurisé à un attribut
    def safe_get(tag, attr):
        try:
            return tag.get(attr, '')
        except Exception:
            return ''

    # Supprimer les balises <script> dont l'attribut src contient "web.archive.org"
    for tag in soup.find_all('script'):
        src = safe_get(tag, 'src')
        if src and "web.archive.org" in src:
            tag.decompose()

    # Supprimer les balises <link> dont l'attribut href contient "web.archive.org"
    for tag in soup.find_all('link'):
        href = safe_get(tag, 'href')
        if href and "web.archive.org" in href:
            tag.decompose()

    # Supprimer les balises <iframe> dont l'attribut src contient "web.archive.org"
    for tag in soup.find_all('iframe'):
        src = safe_get(tag, 'src')
        if src and "web.archive.org" in src:
            tag.decompose()

    # Supprimer tout élément dont l'id commence par "wm-" (ex: barre d'outils Wayback)
    for tag in soup.find_all(id=re.compile(r'^wm-')):
        tag.decompose()

    # Nettoyer les attributs href ou src contenant encore le préfixe Wayback
    for tag in soup.find_all():
        for attr in ['href', 'src']:
            if tag.has_attr(attr):
                val = safe_get(tag, attr)
                if val and "web.archive.org" in val:
                    # On retire le préfixe Wayback : suppression de "https://web.archive.org/web/<timestamp>/"
                    new_val = re.sub(r'https?://web\.archive\.org/web/\d+/', '', val)
                    tag[attr] = new_val

    # Enregistrer le fichier modifié
    try:
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Fichier traité: {filepath}")
    except Exception as e:
        print(f"Erreur lors de l'écriture de {filepath} : {e}")

def process_directory(root_dir):
    for current_path, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.html', '.htm')):
                filepath = os.path.join(current_path, file)
                process_html_file(filepath)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python remove_wayback.py <dossier_site>")
        sys.exit(1)
    root_directory = sys.argv[1]
    process_directory(root_directory)


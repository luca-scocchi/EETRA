import os
import re

html_files = [
    r'c:\Users\Utente\Desktop\Sito Eetra\index.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\servizi.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\impact.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\contatti.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\governance.html',
]

def update_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Academy from nav (Desktop)
    content = re.sub(r'<li><a href="academy\.html".*?Academy</a></li>\s*', '', content, flags=re.IGNORECASE)
    
    # 2. Remove Academy from nav (Mobile)
    content = re.sub(r'<a href="academy\.html".*?Academy</a>\s*', '', content, flags=re.IGNORECASE)

    # 3. Rename Relazione to Governance in links
    content = content.replace('relazioni-di-impatto.html', 'governance.html')
    content = content.replace("Relazione d'Impatto", 'Governance')
    
    # 4. Remove Academy from footer or other places if it's a standalone link
    content = re.sub(r'<a href="academy\.html".*?>.*?Academy.*?</a>\s*', '', content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in html_files:
    if os.path.exists(f):
        update_html(f)
        print(f"Updated {f}")
    else:
        print(f"File not found: {f}")

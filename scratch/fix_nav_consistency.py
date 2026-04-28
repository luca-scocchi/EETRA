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

def update_nav(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the target nav links block
    # We want to replace the entire <ul class="nav__links" role="list">...</ul> block
    
    file_name = os.path.basename(file_path)
    
    nav_links = [
        ('chi-siamo.html', 'Chi siamo'),
        ('servizi.html', 'Servizi'),
        ('impact.html', 'Impact'),
        ('governance.html', 'Governance'),
        ('contatti.html', 'Contatti')
    ]
    
    new_links_html = '      <ul class="nav__links" role="list">\n'
    for href, text in nav_links:
        active_class = ' active' if href == file_name or (file_name == 'index.html' and href == 'index.html') else ''
        new_links_html += f'        <li><a href="{href}" class="nav__link{active_class}">{text}</a></li>\n'
    new_links_html += '      </ul>'

    # Replace the block
    content = re.sub(r'<ul class="nav__links" role="list">.*?</ul>', new_links_html, content, flags=re.DOTALL)

    # Also check mobile menu
    mobile_links = [
        ('chi-siamo.html', 'Chi siamo'),
        ('servizi.html', 'Servizi'),
        ('impact.html', 'Impact'),
        ('governance.html', 'Governance'),
        ('contatti.html', 'Contatti')
    ]
    
    # Identify the mobile menu block and replace links
    # Assuming mobile links are directly inside <div class="nav__mobile" ...>
    # Find the mobile menu div content
    mobile_match = re.search(r'(<div class="nav__mobile".*?>)(.*?)(<div class="nav__mobile-cta")', content, flags=re.DOTALL)
    if mobile_match:
        header = mobile_match.group(1)
        cta = mobile_match.group(3)
        new_mobile_links = '\n'
        for href, text in mobile_links:
            new_mobile_links += f'    <a href="{href}" class="nav__mobile-link">{text}</a>\n'
        new_mobile_links += '    '
        content = content.replace(mobile_match.group(0), header + new_mobile_links + cta)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in html_files:
    if os.path.exists(f):
        update_nav(f)
        print(f"Updated nav in {f}")
    else:
        print(f"File not found: {f}")

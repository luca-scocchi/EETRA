import os

pages = [
    r'c:\Users\Utente\Desktop\Sito Eetra\index.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\servizi.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\academy.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\impact.html',
    r'c:\Users\Utente\Desktop\Sito Eetra\contatti.html',
]

replacements = [
    # Desktop nav: add Relazione link before Contatti
    (
        '<li><a href="impact.html"     class="nav__link">Impact</a></li>\n      <li><a href="contatti.html"   class="nav__link">Contatti</a></li>',
        '<li><a href="impact.html"     class="nav__link">Impact</a></li>\n      <li><a href="relazioni-di-impatto.html" class="nav__link">Relazione d\'Impatto</a></li>\n      <li><a href="contatti.html"   class="nav__link">Contatti</a></li>'
    ),
    # Mobile menu: add Relazione link
    (
        '<a href="impact.html"     class="nav__mobile-link">Impact</a>\n  <a href="contatti.html"   class="nav__mobile-link">Contatti</a>',
        '<a href="impact.html"     class="nav__mobile-link">Impact</a>\n  <a href="relazioni-di-impatto.html" class="nav__mobile-link">Relazione d\'Impatto</a>\n  <a href="contatti.html"   class="nav__mobile-link">Contatti</a>'
    ),
    # Footer nav: add Relazione link
    (
        '<a href="impact.html">Impact &amp; News</a>\n          <a href="contatti.html">Contatti</a>',
        '<a href="impact.html">Impact &amp; News</a>\n          <a href="relazioni-di-impatto.html">Relazione d\'Impatto</a>\n          <a href="contatti.html">Contatti</a>'
    ),
]

for path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    changed = content != original
    print(f'{os.path.basename(path)}: {"UPDATED" if changed else "no change"}')

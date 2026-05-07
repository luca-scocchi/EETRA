import re

with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Team data: (name, role, initials, [certs])
team = [
    ("Carlo Rossini",       "CEO & Partner",           "CR", []),
    ("Martina Castoldi",    "Partner",                 "MC", []),
    ("Michela Fancello",    "Partner",                 "MF", []),
    ("Guido Rossini",       "CFO Finance Lead",        "GR", ["LEED AP EBOM", "EGE"]),
    ("Chiara La Fortezza",  "Sustainability Player",   "CF", ["B Leader"]),
    ("Andrea Botti",        "CTO Technical Lead",      "AB", ["LEED AP BD+C", "PhD"]),
    ("Giulia Rossetti",     "Sustainability Player",   "GR", ["LEED GA"]),
    ("Letizia Garbolino",   "Sustainability Expert",   "LG", ["LEED AP ID+C", "WELL AP", "SITES AP", "Access4you"]),
    ("Gianluca Buccheri",   "Sustainability Player",   "GB", ["LEED GA"]),
    ("Chiara Cortellazzi",  "Sustainability Expert",   "CC", ["LEED AP BD+C", "WELL AP", "Wiredscore AP"]),
    ("Souzan Goloburda",    "Sustainability Junior",   "SG", []),
]

def make_card(i, name, role, initials, certs):
    delays = ['', ' delay-1', ' delay-2', ' delay-3']
    d = delays[i % 4]
    
    certs_html = ''
    if certs:
        badges = '\n              '.join(f'<span class="cert-badge">{c}</span>' for c in certs)
        certs_html = f'''
            <div class="team-card__certs">
              {badges}
            </div>'''
    
    return f'''        <div class="team-card{d}">
          <div class="team-card__photo"><div class="team-card__photo-placeholder">{initials}</div></div>
          <div class="team-card__body">
            <p class="team-card__name">{name}</p>
            <p class="team-card__role">{role}</p>{certs_html}
          </div>
        </div>'''

cards = [make_card(i, *t) for i, t in enumerate(team)]

new_grid = '      <div class="grid-4 fade-up">\n'
new_grid += '\n'.join(cards)
new_grid += '\n      </div>'

# Find and replace the grid-4 block
content_n = content.replace('\r\n', '\n')

# Use regex to find the grid-4 team block
pattern = r'      <div class="grid-4 fade-up">\n.*?      </div>'
match = re.search(pattern, content_n, re.DOTALL)

if match:
    new_content = content_n[:match.start()] + new_grid + content_n[match.end():]
    with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"SUCCESS: {len(team)} team cards written with real names.")
else:
    print("ERROR: Could not find grid-4 block")

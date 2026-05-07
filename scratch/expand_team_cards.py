import re

with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_grid = '''      <div class="grid-4 fade-up">
        <!-- Team member cards (placeholder names - da completare con team reale) -->
        <div class="team-card">
          <div class="team-card__photo">
            <div class="team-card__photo-placeholder">ET</div>
          </div>
          <div class="team-card__body">
            <p class="team-card__name">Team EETRA</p>
            <p class="team-card__role">ESG Senior Consultant</p>
            <div class="team-card__certs">
              <span class="cert-badge">LEED AP BD+C</span>
              <span class="cert-badge">B Leader</span>
            </div>
          </div>
        </div>
        <div class="team-card delay-1">
          <div class="team-card__photo">
            <div class="team-card__photo-placeholder">ET</div>
          </div>
          <div class="team-card__body">
            <p class="team-card__name">Team EETRA</p>
            <p class="team-card__role">Sustainability Manager</p>
            <div class="team-card__certs">
              <span class="cert-badge">BREEAM Assessor</span>
              <span class="cert-badge">GRI Expert</span>
            </div>
          </div>
        </div>
        <div class="team-card delay-2">
          <div class="team-card__photo">
            <div class="team-card__photo-placeholder">ET</div>
          </div>
          <div class="team-card__body">
            <p class="team-card__name">Team EETRA</p>
            <p class="team-card__role">Carbon Specialist</p>
            <div class="team-card__certs">
              <span class="cert-badge">WELL AP</span>
              <span class="cert-badge">LEED AP ID+C</span>
            </div>
          </div>
        </div>
        <div class="team-card delay-3">
          <div class="team-card__photo">
            <div class="team-card__photo-placeholder">ET</div>
          </div>
          <div class="team-card__body">
            <p class="team-card__name">Team EETRA</p>
            <p class="team-card__role">ESG Reporting Expert</p>
            <div class="team-card__certs">
              <span class="cert-badge">Envision SP</span>
              <span class="cert-badge">LEED AP O+M</span>
            </div>
          </div>
        </div>
      </div>'''

def card(delay, role, cert1, cert2):
    d = f' delay-{delay}' if delay else ''
    return f'''        <div class="team-card{d}">
          <div class="team-card__photo"><div class="team-card__photo-placeholder">ET</div></div>
          <div class="team-card__body">
            <p class="team-card__name">Team EETRA</p>
            <p class="team-card__role">{role}</p>
            <div class="team-card__certs">
              <span class="cert-badge">{cert1}</span>
              <span class="cert-badge">{cert2}</span>
            </div>
          </div>
        </div>'''

cards = [
    card('',  'ESG Senior Consultant',       'LEED AP BD+C',   'B Leader'),
    card('1', 'Sustainability Manager',       'BREEAM AP',      'GRI Expert'),
    card('2', 'Carbon Specialist',            'WELL AP',        'LEED AP ID+C'),
    card('3', 'ESG Reporting Expert',         'Envision SP',    'LEED AP O+M'),
    card('1', 'Energy Manager',               'EGE UNI 11339',  'BREEAM In Use'),
    card('2', 'Gender Equity Auditor',        'PDR 125',        'Sustainability Mgr'),
    card('3', 'Green Building Consultant',    'LEED AP BD+C',   'Fitwel Ambassador'),
    card('',  'BREEAM Assessor',              'BREEAM NC',      'BREEAM RFO'),
    card('1', 'Esperto CAM',                  'ISO IEC 17024',  'WiredScore AP'),
    card('2', 'Impact Measurement',           'GRI Expert',     'B Leader'),
    card('3', 'Strategia ESG & Comunicazione','PDR 109',        'Envision SP'),
    card('',  'Rigenerazione Urbana',         'WELL AP',        'LEED AP BD+C'),
]

new_grid = '      <div class="grid-4 fade-up">\n        <!-- Team member cards — da completare con nomi e foto reali -->\n'
new_grid += '\n'.join(cards)
new_grid += '\n      </div>'

# Normalize line endings for matching
old_normalized = old_grid.replace('\r\n', '\n').replace('\r', '\n')
content_normalized = content.replace('\r\n', '\n').replace('\r', '\n')

if old_normalized in content_normalized:
    new_content = content_normalized.replace(old_normalized, new_grid, 1)
    with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: 12 team cards written.")
else:
    # Fallback: replace by line markers
    print("FALLBACK: exact match not found, trying line-based replacement...")
    lines = content_normalized.split('\n')
    start = None
    end = None
    for i, line in enumerate(lines):
        if 'grid-4 fade-up' in line and start is None:
            start = i
        if start is not None and line.strip() == '</div>' and i > start + 5:
            # find the closing </div> of grid-4
            depth = 0
            for j in range(start, len(lines)):
                depth += lines[j].count('<div') - lines[j].count('</div>')
                if j > start and depth == 0:
                    end = j
                    break
            break
    if start is not None and end is not None:
        new_lines = lines[:start] + new_grid.split('\n') + lines[end+1:]
        with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"SUCCESS via fallback: replaced lines {start}-{end}")
    else:
        print("ERROR: Could not find grid-4 section")

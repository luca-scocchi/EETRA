"""
Merge governance.html content into chi-siamo.html:
1. Copy governance CSS styles into chi-siamo <head>
2. Insert governance sections before CTA in chi-siamo
3. Copy handleDownload script
4. Remove 'Governance' from nav in ALL pages
5. Update chi-siamo nav to mark it active for governance too
"""
import re, glob

# ── Read files ──
with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'r', encoding='utf-8') as f:
    chi = f.read()
with open(r'c:\Users\Utente\Desktop\Sito Eetra\governance.html', 'r', encoding='utf-8') as f:
    gov = f.read()

# ── 1. Extract governance styles ──
style_match = re.search(r'<style>(.*?)</style>', gov, re.DOTALL)
gov_styles = style_match.group(1) if style_match else ''

# Also get the responsive media query at the bottom
media_match = re.search(r'<style>\s*@media.*?</style>', gov, re.DOTALL)
gov_media = media_match.group(0) if media_match else ''

# ── 2. Build governance sections HTML ──
governance_html = """
  <!-- ============================================================
     GOVERNANCE
     ============================================================ -->
  <section class="section th-cream" id="governance" aria-label="Governance">
    <div class="container">
      <div class="sec-label fade-up"><span>Governance</span></div>
      <h2 class="t-h2 mb-4 fade-up" style="color:var(--dark)">
        Il nostro impatto misurabile,<br>ogni anno
      </h2>
      <p class="fade-up delay-1" style="font-size:1.0625rem; color:var(--muted-dk); line-height:1.65; max-width:720px; margin-bottom:3rem">
        Come Società Benefit certificata B Corp, EETRA pubblica ogni anno la Governance: un documento trasparente che rendiconta l'impatto ambientale, sociale e di governance generato dalla nostra attività e dai nostri progetti.
      </p>

      <!-- Stats strip -->
      <div class="grid-3 fade-up" style="gap:0; border:1px solid var(--border-lt); border-radius:var(--r-md); margin-bottom:3.5rem">
        <div style="padding:2rem 2.5rem; border-right:1px solid var(--border-lt)">
          <div style="font-family:var(--font-serif); font-size:2.25rem; font-weight:700; color:var(--green)">86,7</div>
          <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-dk); margin-top:0.3rem">Punteggio B Corp 2024</p>
        </div>
        <div style="padding:2rem 2.5rem; border-right:1px solid var(--border-lt)">
          <div style="font-family:var(--font-serif); font-size:2.25rem; font-weight:700; color:var(--green)">Annuale</div>
          <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-dk); margin-top:0.3rem">Frequenza di pubblicazione</p>
        </div>
        <div style="padding:2rem 2.5rem">
          <div style="font-family:var(--font-serif); font-size:2.25rem; font-weight:700; color:var(--green)">PDF</div>
          <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-dk); margin-top:0.3rem">Formato download gratuito</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================
     GOVERNANCE REPORTS
     ============================================================ -->
  <section class="section th-dark" id="reports" aria-label="Archivio Relazioni d'Impatto">
    <div class="container">
      <div class="sec-label sec-label--lt"><span>Archivio report</span></div>
      <h2 class="t-h2 mb-8 fade-up">
        Scarica le nostre<br>Relazioni d'Impatto
      </h2>

      <div class="grid-3 fade-up">

        <!-- Report 2024 (LATEST) -->
        <article class="report-card">
          <div class="report-card__cover">
            <div class="report-card__cover-placeholder">
              <div style="font-size:2.5rem; opacity:0.4">📄</div>
              <div class="report-card__cover-year">2024</div>
              <p class="report-card__cover-label">Governance</p>
              <div style="display:inline-block; padding:0.3rem 0.9rem; border:1px solid rgba(92,123,42,0.4); border-radius:100px; font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--green-pale)">Edizione più recente</div>
            </div>
            <div class="report-card__cover-bar"></div>
          </div>
          <div class="report-card__body">
            <div class="report-card__score">
              <span class="report-card__score-val">86,7</span>
              <span class="report-card__score-lbl">B Corp Score</span>
            </div>
            <h3 class="report-card__title">Governance EETRA 2024</h3>
            <p class="report-card__desc">
              Il report annuale documenta l'impatto generato da EETRA nel 2024: progetti ESG completati, emissioni evitate, clienti supportati, formazione erogata e governance interna.
            </p>
            <div class="report-card__actions">
              <a href="#" class="btn btn-primary" id="download-2024" download onclick="handleDownload(event, '2024')">
                Download PDF <span class="arrow">→</span>
              </a>
            </div>
          </div>
        </article>

        <!-- Report 2023 -->
        <article class="report-card">
          <div class="report-card__cover">
            <div class="report-card__cover-placeholder">
              <div style="font-size:2.5rem; opacity:0.3">📄</div>
              <div class="report-card__cover-year" style="color:var(--muted-lt)">2023</div>
              <p class="report-card__cover-label">Governance</p>
            </div>
          </div>
          <div class="report-card__body">
            <div class="report-card__score" style="opacity:0.8">
              <span class="report-card__score-val" style="color:var(--muted-lt)">82,4</span>
              <span class="report-card__score-lbl">B Corp Score</span>
            </div>
            <h3 class="report-card__title" style="color:var(--muted-lt)">Governance EETRA 2023</h3>
            <p class="report-card__desc">
              Report annuale 2023: espansione del team, nuove certificazioni LEED e BREEAM completate e primo anno come Sustainability Consultancy B Corp in Italia.
            </p>
            <div class="report-card__actions">
              <a href="#" class="btn btn-outline" id="download-2023" download onclick="handleDownload(event, '2023')">
                Download PDF <span class="arrow">→</span>
              </a>
            </div>
          </div>
        </article>

        <!-- Report 2022 -->
        <article class="report-card" style="opacity:0.65">
          <div class="report-card__cover">
            <div class="report-card__cover-placeholder">
              <div style="font-size:2.5rem; opacity:0.2">📄</div>
              <div class="report-card__cover-year" style="color:var(--muted-dk)">2022</div>
              <p class="report-card__cover-label">Governance</p>
            </div>
          </div>
          <div class="report-card__body">
            <div class="report-card__score" style="opacity:0.6">
              <span class="report-card__score-val" style="color:var(--muted-dk)">79,1</span>
              <span class="report-card__score-lbl">B Corp Score</span>
            </div>
            <h3 class="report-card__title" style="color:var(--muted-dk)">Governance EETRA 2022</h3>
            <p class="report-card__desc" style="color:var(--muted-dk)">
              Report annuale 2022: consolidamento servizi ESG, avvio percorso B Corp, crescita del portafoglio clienti nel real estate sostenibile.
            </p>
            <div class="report-card__actions">
              <a href="#" class="btn btn-outline" style="opacity:0.6">
                Download PDF <span class="arrow">→</span>
              </a>
            </div>
          </div>
        </article>

      </div>
    </div>
  </section>

  <!-- ============================================================
     COSA CONTIENE LA GOVERNANCE
     ============================================================ -->
  <section class="section th-cream" aria-label="Cosa contiene la governance">
    <div class="container">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:5rem; align-items:start" class="responsive-split">
        <div class="fade-up">
          <div class="sec-label"><span>Il contenuto</span></div>
          <h2 class="t-h2 mb-4" style="color:var(--dark)">
            Cosa trovi nella<br>Governance
          </h2>
          <p style="font-size:1rem; color:var(--muted-dk); line-height:1.72; margin-bottom:1.25rem">
            La Governance di EETRA è redatta secondo le linee guida per le Società Benefit e i requisiti B Corp. Non è un documento di marketing: è una rendicontazione trasparente e verificabile.
          </p>
          <p style="font-size:1rem; color:var(--muted-dk); line-height:1.72">
            I dati vengono raccolti internamente, validati dal team ESG e sottoposti a verifica nell'ambito del processo di recertificazione B Corp annuale.
          </p>
        </div>

        <div class="fade-up delay-1">
          <div class="step-item">
            <span class="step-n">01</span>
            <div class="step-content">
              <h4 class="step-title">Impatto ambientale</h4>
              <p class="step-desc">Emissioni di CO₂, consumi energetici, riduzione emissioni generata dai progetti ESG per i clienti, certificazioni ambientali.</p>
            </div>
          </div>
          <div class="step-item">
            <span class="step-n">02</span>
            <div class="step-content">
              <h4 class="step-title">Impatto sociale</h4>
              <p class="step-desc">Ore di formazione, professionisti formati, iniziative di welfare, diversità e inclusione del team.</p>
            </div>
          </div>
          <div class="step-item">
            <span class="step-n">03</span>
            <div class="step-content">
              <h4 class="step-title">Governance</h4>
              <p class="step-desc">Struttura societaria, mission benefit, politiche di trasparenza, gestione dei fornitori secondo criteri ESG.</p>
            </div>
          </div>
          <div class="step-item">
            <span class="step-n">04</span>
            <div class="step-content">
              <h4 class="step-title">Punteggio B Corp</h4>
              <p class="step-desc">B Impact Score complessivo e per categoria: Community, Environment, Workers, Customers, Governance.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# ── 3. Insert governance CSS into chi-siamo <head> ──
css_insert = f"<style>{gov_styles}</style>\n"
# Also add responsive media query
css_insert += "\n<style>\n@media (max-width:768px) { .responsive-split { grid-template-columns:1fr !important; gap:3rem !important; } }\n</style>\n"

# Insert before </head>
chi = chi.replace('</head>', css_insert + '</head>')

# ── 4. Insert governance HTML before the CTA section ──
cta_marker = '  <!-- ============================================================\n     CTA'
if cta_marker not in chi:
    # Try with \r\n
    cta_marker = '  <!-- ============================================================\r\n     CTA'

chi = chi.replace(cta_marker, governance_html + '\n' + cta_marker)

# ── 5. Add handleDownload script before </body> ──
download_script = """
<script>
function handleDownload(e, year) {
  var link = document.getElementById('download-' + year);
  if (!link || link.getAttribute('href') === '#') {
    e.preventDefault();
    alert('Il PDF della Relazione d\\'Impatto ' + year + ' non è ancora stato caricato. Contattaci a info@eetra.it per riceverlo.');
  }
}
</script>
"""
chi = chi.replace('</body>', download_script + '</body>')

# ── 6. Write updated chi-siamo.html ──
with open(r'c:\Users\Utente\Desktop\Sito Eetra\chi-siamo.html', 'w', encoding='utf-8') as f:
    f.write(chi)
print("SUCCESS: Governance content merged into chi-siamo.html")

# ── 7. Remove 'Governance' nav link from ALL pages ──
html_files = glob.glob(r'c:\Users\Utente\Desktop\Sito Eetra\*.html')
for fp in html_files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Remove desktop nav link
    for pattern in [
        '<li><a href="governance.html" class="nav__link active">Governance</a></li>\r\n',
        '<li><a href="governance.html" class="nav__link active">Governance</a></li>\n',
        '<li><a href="governance.html" class="nav__link">Governance</a></li>\r\n',
        '<li><a href="governance.html" class="nav__link">Governance</a></li>\n',
        '        <li><a href="governance.html" class="nav__link active">Governance</a></li>\r\n',
        '        <li><a href="governance.html" class="nav__link active">Governance</a></li>\n',
        '        <li><a href="governance.html" class="nav__link">Governance</a></li>\r\n',
        '        <li><a href="governance.html" class="nav__link">Governance</a></li>\n',
    ]:
        if pattern in content:
            content = content.replace(pattern, '')
            modified = True
    
    # Remove mobile nav link
    for pattern in [
        '<a href="governance.html" class="nav__mobile-link">Governance</a>\r\n',
        '<a href="governance.html" class="nav__mobile-link">Governance</a>\n',
        '    <a href="governance.html" class="nav__mobile-link">Governance</a>\r\n',
        '    <a href="governance.html" class="nav__mobile-link">Governance</a>\n',
    ]:
        if pattern in content:
            content = content.replace(pattern, '')
            modified = True
    
    # Remove footer governance link
    for pattern in [
        '<a href="governance.html">Governance</a>\r\n',
        '<a href="governance.html">Governance</a>\n',
        '          <a href="governance.html">Governance</a>\r\n',
        '          <a href="governance.html">Governance</a>\n',
    ]:
        if pattern in content:
            content = content.replace(pattern, '')
            modified = True
    
    if modified:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Nav updated: {fp.split(chr(92))[-1]}")

print("DONE: All navigation links updated.")

with open('chi-siamo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find boundaries
start_search = 'WHAT WE DO'
end_search = 'MISSION'
start_idx = content.rfind('<!--', 0, content.find(start_search))
end_idx = content.rfind('<!--', 0, content.find(end_search))

new_sections = '''  <!-- ============================================================
     WHO WE ARE
     ============================================================ -->
  <section class="section" id="who-we-are" aria-label="Chi siamo - identità">
    <div class="container">
      <div class="sec-label"><span>Who we are</span></div>
      <h2 class="t-h2 fade-up" style="max-width:820px; margin-bottom:3rem">
        Siamo una Società Benefit certificata B Corp, nata per definire nuovi modelli sostenibili e rigenerativi.
      </h2>
      <div class="grid-2 fade-up delay-1" style="gap:4rem; align-items:start; border-top:1px solid var(--border); padding-top:3rem">
        <div>
          <p style="font-size:1.0625rem; line-height:1.75; color:var(--muted-dk); margin-bottom:1.5rem">
            Crediamo nella transizione da un&apos;economia estrattiva a un&apos;economia rigenerativa. Un futuro in cui ogni impresa contribuisce alla generazione di valore condiviso e duraturo.
          </p>
          <p style="font-size:1rem; line-height:1.65; color:var(--muted-dk)">
            Il nostro approccio integra <strong style="color:var(--dark)">strategia, innovazione e consulenza operativa</strong> in ambito ESG.
          </p>
        </div>
        <div>
          <p style="font-size:0.8125rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--dark); margin-bottom:1.5rem; opacity:0.5">Guidiamo aziende, enti, persone e territori</p>
          <ul style="list-style:none; padding:0; margin:0">
            <li style="display:flex; gap:1rem; align-items:flex-start; padding:1.25rem 0; border-bottom:1px solid var(--border)">
              <span style="color:var(--olive); font-weight:700; font-size:1rem; flex-shrink:0; margin-top:0.1rem">01</span>
              <span style="color:var(--muted-dk); line-height:1.65">Nel progettare percorsi di cambiamento sistemico, integrando la rigenerazione nei processi, nei prodotti e nelle relazioni.</span>
            </li>
            <li style="display:flex; gap:1rem; align-items:flex-start; padding:1.25rem 0">
              <span style="color:var(--olive); font-weight:700; font-size:1rem; flex-shrink:0; margin-top:0.1rem">02</span>
              <span style="color:var(--muted-dk); line-height:1.65">Nel misurare, migliorare e comunicare il proprio impatto positivo.</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================
     WHAT WE DO — LE NOSTRE ATTIVITÀ (OVERVIEW)
     ============================================================ -->
  <section class="section th-cream" id="attivita" aria-label="Le nostre attività">
    <div class="container">
      <div class="sec-label"><span>What we do</span></div>
      <h2 class="t-h2 mb-2 fade-up" style="color:var(--dark)">Le nostre attività</h2>
      <p class="fade-up delay-1" style="font-size:1.0625rem; color:var(--muted-dk); max-width:660px; margin-bottom:3.5rem; line-height:1.7">
        Il nostro approccio è orientato a superare modelli lineari ed affrontare le sfide normative, climatiche e sociali promuovendo competitività, resilienza e circolarità.
      </p>
      <div class="activity-grid">
        <div class="activity-card fade-up delay-1">
          <div class="activity-card__icon"><img src="infosito/company atlas (1).png" alt="Company Atlas"></div>
          <h3 class="activity-card__title">Company Atlas</h3>
          <p class="activity-card__text">La mappa strategica per le esigenze ESG di organizzazioni, brands, processi e servizi.</p>
        </div>
        <div class="activity-card fade-up delay-2">
          <div class="activity-card__icon"><img src="infosito/positive impact.png" alt="Positive Impact"></div>
          <h3 class="activity-card__title">Positive Impact</h3>
          <p class="activity-card__text">Gli strumenti e le certificazioni per la trasformazione rigenerativa di prodotti.</p>
        </div>
        <div class="activity-card fade-up delay-3">
          <div class="activity-card__icon"><img src="infosito/environmental intelligence.png" alt="Environmental Intelligence"></div>
          <h3 class="activity-card__title">Environmental Intelligence</h3>
          <p class="activity-card__text">I protocolli per la decarbonizzazione e la transizione rigenerativa del settore immobiliare ed infrastrutture.</p>
        </div>
        <div class="activity-card fade-up delay-4">
          <div class="activity-card__icon"><img src="infosito/innovation engine.png" alt="Innovation Engine"></div>
          <h3 class="activity-card__title">Innovation Engine</h3>
          <p class="activity-card__text">Laboratorio per sperimentare e scalare soluzioni innovative basate su dati, modelli e automazioni.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================
     WHAT WE DO — COMPANY ATLAS DETTAGLIO
     ============================================================ -->
  <section class="section" id="company-atlas-detail" aria-label="Company Atlas nel dettaglio">
    <div class="container">
      <div class="sec-label"><span>What we do · Company Atlas</span></div>
      <div style="display:flex; align-items:center; gap:1.25rem; margin-bottom:1.25rem" class="fade-up">
        <img src="infosito/company atlas (1).png" alt="Company Atlas" style="height:52px; width:auto">
        <h2 class="t-h2" style="margin:0">Company Atlas</h2>
      </div>
      <p class="fade-up delay-1" style="font-size:1.125rem; color:var(--muted-dk); max-width:700px; margin-bottom:3.5rem; line-height:1.7">
        La mappa strategica per le esigenze ESG di organizzazioni, brands, processi e servizi. Pensato per PMI, aziende di servizi, manifattura e produzione.
      </p>
      <div class="grid-2 fade-up delay-2" style="gap:4rem; align-items:start">
        <div>
          <p style="font-size:0.8125rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--dark); margin-bottom:1.25rem; opacity:0.5">Servizi</p>
          <ul style="list-style:none; padding:0; margin:0">
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Fractional ESG management</li>
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Rendicontazione volontaria VSME e Relazione di Impatto</li>
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Certificazioni (UNI PdR 125, SA8000, B CORP, ISO 14001, ISO 50001)</li>
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:flex-start; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0; margin-top:0.45rem"></span>Stesura politiche (DE&amp;I, Supply Chain, Codice Etico, Politica Gestione Ambientale, Decarbonizzazione)</li>
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Engagement, comunicazione e marketing ESG</li>
            <li style="padding:0.875rem 0; border-bottom:1px solid var(--border); display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Decarbonizzazione (GHG Footprint Scope 1, 2 e 3)</li>
            <li style="padding:0.875rem 0; display:flex; gap:0.875rem; align-items:center; font-size:0.9875rem; color:var(--dark); line-height:1.5"><span style="width:6px; height:6px; background:var(--olive); border-radius:50%; flex-shrink:0"></span>Formazione on-demand</li>
          </ul>
          <div style="margin-top:2rem">
            <a href="servizi.html#company-atlas" class="btn btn-primary">Scopri Company Atlas <span class="arrow">→</span></a>
          </div>
        </div>
        <div>
          <p style="font-size:0.8125rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--dark); margin-bottom:1.25rem; opacity:0.5">Clienti principali</p>
          <div style="display:flex; flex-wrap:wrap; gap:0.5rem">
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Hilti Italia</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Olmetex</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Fenzi Group</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Save the Children</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Emsibeth</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Trenord</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Malpensa Intermodale</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">IMCD Italia</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Slalom Acoustic</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">TermoIsover</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Tundr Tech</span>
            <span style="background:var(--cream); border:1px solid var(--border); border-radius:100px; padding:0.35rem 0.875rem; font-size:0.875rem; color:var(--dark)">Unicalce</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================================
     WHY CHOOSE US
     ============================================================ -->
  <section class="section th-dark" id="why-choose-us" aria-label="Perché scegliere EETRA">
    <div class="container">
      <div class="sec-label sec-label--lt"><span>Why choose us</span></div>
      <h2 class="t-h2 mb-4 fade-up" style="color:var(--off-white)">Rigenerare significa rendere le imprese più capaci di competere nel lungo periodo.</h2>
      <p class="fade-up delay-1" style="font-size:1.0625rem; color:var(--muted-lt); max-width:680px; margin-bottom:3.5rem; line-height:1.7">
        Il nostro approccio è orientato a superare modelli lineari ed affrontare le sfide normative, climatiche e sociali promuovendo competitività, resilienza e circolarità per progetti e modelli di business.
      </p>
      <div class="grid-2 fade-up delay-2" style="gap:3rem; align-items:start; border-top:1px solid var(--border-dk); padding-top:3rem">
        <div>
          <p style="font-size:0.8125rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-lt); margin-bottom:1.5rem; opacity:0.7">Le imprese che integrano criteri ESG:</p>
          <ul style="list-style:none; padding:0; margin:0">
            <li style="padding:1rem 0; border-bottom:1px solid var(--border-dk); color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Ridimensionano i rischi reputazionali, operativi e finanziari</li>
            <li style="padding:1rem 0; border-bottom:1px solid var(--border-dk); color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Aumentano la capacità di adattarsi ai cambiamenti di mercato e regolatori</li>
            <li style="padding:1rem 0; border-bottom:1px solid var(--border-dk); color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Rafforzano la continuità operativa e la fiducia degli stakeholders</li>
            <li style="padding:1rem 0; color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Migliorano il posizionamento competitivo, distinguendosi nel mercato</li>
          </ul>
        </div>
        <div>
          <p style="font-size:0.8125rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--muted-lt); margin-bottom:1.5rem; opacity:0.7">Il nostro lavoro: tradurre la visione rigenerativa in leve strategiche</p>
          <ul style="list-style:none; padding:0; margin:0">
            <li style="padding:1rem 0; border-bottom:1px solid var(--border-dk); color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Progettando roadmap coerenti e scalabili</li>
            <li style="padding:1rem 0; border-bottom:1px solid var(--border-dk); color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Valorizzando la cultura organizzativa e la comunicazione trasparente</li>
            <li style="padding:1rem 0; color:var(--muted-lt); line-height:1.6; display:flex; gap:0.875rem"><span style="color:#b8c98a; flex-shrink:0">→</span>Accompagnando ogni cliente nel connettere sostenibilità, riduzione del rischio e performance economica</li>
          </ul>
          <div style="margin-top:2rem">
            <a href="contatti.html" class="btn btn-primary">Richiedi consulenza <span class="arrow">→</span></a>
          </div>
        </div>
      </div>
    </div>
  </section>

  '''

new_content = content[:start_idx] + new_sections + content[end_idx:]

with open('chi-siamo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done! File updated successfully.')
# verify
with open('chi-siamo.html', 'r', encoding='utf-8') as f:
    updated = f.read()
print(f'New file length: {len(updated)} chars')
print('Contains who-we-are:', 'who-we-are' in updated)
print('Contains company-atlas-detail:', 'company-atlas-detail' in updated)
print('Contains why-choose-us:', 'why-choose-us' in updated)
print('Old strategic guide gone:', 'guida-strategica' not in updated)

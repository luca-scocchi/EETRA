"""
EETRA — Genera Alberatura Sito Web (PDF)
Orientamento: A3 Landscape · Palette EETRA
Fix: L3 posizionamento sequenziale (no centrato-sul-padre → no overlap)
"""

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
import os

# ── Palette EETRA ─────────────────────────────────────────────────────────────
DARK        = HexColor("#191C11")
DARK2       = HexColor("#23271A")
DARK3       = HexColor("#2E3320")
GREEN       = HexColor("#5C7B2A")
GREEN_HOVER = HexColor("#33b149")
GREEN_PALE  = HexColor("#B5D282")
OFF_WHITE   = HexColor("#F6F3ED")
MUTED_DK    = HexColor("#6A6D5E")
MUTED_LT    = HexColor("#9E9F92")

COLOR_CORE   = HexColor("#5C7B2A")
COLOR_IMPACT = HexColor("#2E7D5E")
COLOR_GOV    = HexColor("#2A5E7D")
COLOR_WHY    = HexColor("#8A6D2F")

# ── Output ────────────────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(__file__), "alberatura_sito.pdf")
W, H = landscape(A3)   # ~1191 x 842 pt
MARGIN = 24 * mm       # margine laterale

# ── Layout ────────────────────────────────────────────────────────────────────
NW     = 136   # larghezza nodo
NH     = 32    # altezza nodo L1
NH_SM  = 19    # altezza nodo L2
NH_L3  = 15    # altezza nodo L3 (compatto)
NH_BIG = 44    # altezza nodo HOME
GAP_X  = 20    # spazio orizzontale tra colonne
GAP_Y  = 6     # spazio verticale tra nodi L2
GAP_Y3 = 4     # spazio verticale tra nodi L3
GAP_L1 = 118   # spazio verticale tra rami L1

HEADER_H = 32 * mm
FOOTER_H = 14 * mm

COL0 = MARGIN
COL1 = COL0 + NW + GAP_X
COL2 = COL1 + NW + GAP_X
COL3 = COL2 + NW + GAP_X

# area verticale utile (in coordinate ReportLab: basso = 0)
TREE_TOP = H - HEADER_H - 38   # top dell'area albero (y alta)
TREE_BOT = FOOTER_H + 10        # bottom dell'area albero (y bassa)


# ── Canvas helpers ────────────────────────────────────────────────────────────
class PDF:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=landscape(A3))
        self.c.setTitle("EETRA — Alberatura Sito Web 2026")
        self.c.setAuthor("EETRA Srl SB")

    def fill(self, col):  self.c.setFillColor(col)
    def stroke(self, col, w=0.5):
        self.c.setStrokeColor(col); self.c.setLineWidth(w)

    def rect(self, x, y, w, h, fill=True, stroke=False, r=4):
        self.c.roundRect(x, y, w, h, r,
                         fill=1 if fill else 0,
                         stroke=1 if stroke else 0)

    def text(self, txt, x, y, size=8, bold=False, color=OFF_WHITE, align="left"):
        self.c.setFillColor(color)
        self.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        if align == "center": self.c.drawCentredString(x, y, txt)
        elif align == "right": self.c.drawRightString(x, y, txt)
        else: self.c.drawString(x, y, txt)

    def save(self): self.c.save(); print(f"PDF salvato: {OUT}")


# ── Primitivi disegno ─────────────────────────────────────────────────────────
def draw_node(pdf, x, y, w, h, label, sublabel="",
              bg=DARK3, text_col=OFF_WHITE, accent=GREEN_PALE, small=False):
    pdf.fill(bg);  pdf.stroke(GREEN, 0.4)
    pdf.rect(x, y, w, h, fill=True, stroke=True, r=4)
    pdf.fill(accent)
    pdf.rect(x, y, 3, h, fill=True, stroke=False, r=0)
    fsz = 6 if small else 7.5
    offset = 4 if sublabel else 1
    pdf.text(label,    x+8, y+h/2+offset, size=fsz,   bold=True,  color=text_col)
    if sublabel:
        pdf.text(sublabel, x+8, y+h/2-5,  size=5,     bold=False, color=MUTED_LT)


def draw_conn(pdf, x1, y1, x2, y2):
    pdf.stroke(MUTED_DK, 0.55)
    c = pdf.c; c.setDash(2, 3)
    mx = (x1 + x2) / 2
    c.line(x1, y1, mx, y1); c.line(mx, y1, mx, y2); c.line(mx, y2, x2, y2)
    c.setDash()


# ── Funzione generica L2 ──────────────────────────────────────────────────────
def draw_l2(pdf, col_x, parent_mid_y, items, bg, accent, return_mids=False):
    """Nodi L2 centrati sul padre — ok perché pochi figli e spazio ampio."""
    n = len(items)
    total = n * NH_SM + (n - 1) * GAP_Y
    start_bot = parent_mid_y + total / 2 - NH_SM   # y_bottom del nodo più in alto

    mids = []
    for i, (lbl, sub) in enumerate(items):
        yb = start_bot - i * (NH_SM + GAP_Y)
        draw_node(pdf, col_x, yb, NW, NH_SM, lbl, sub, bg=bg, accent=accent, small=True)
        mid = yb + NH_SM / 2
        mids.append((mid, bg, accent))
        draw_conn(pdf, col_x - GAP_X, parent_mid_y, col_x, mid)

    return mids if return_mids else None


# ── Funzione L3 SEQUENZIALE ───────────────────────────────────────────────────
def draw_l3_sequential(pdf, col_x, bu_mids, bu_details, avail_top, avail_bot):
    """
    Posiziona tutti i gruppi L3 in sequenza verticale (top→bottom)
    nell'area [avail_bot, avail_top], con un gap tra i gruppi.
    I connettori puntano al rispettivo nodo BU padre.
    """
    GROUP_GAP = 12   # spazio extra tra gruppi diversi

    # Calcola altezza totale necessaria
    heights = []
    for det in bu_details:
        n = len(det)
        heights.append(n * NH_L3 + (n - 1) * GAP_Y3)
    total_needed = sum(heights) + (len(heights) - 1) * GROUP_GAP

    avail_h = avail_top - avail_bot
    # Se non entra, scala i gap
    if total_needed > avail_h:
        scale = avail_h / total_needed
        GROUP_GAP = max(4, int(GROUP_GAP * scale))
        GAP_Y3_use = max(2, int(GAP_Y3 * scale))
    else:
        GAP_Y3_use = GAP_Y3

    # Ricalcola con eventuali gap scalati
    heights = []
    for det in bu_details:
        n = len(det)
        heights.append(n * NH_L3 + (n - 1) * GAP_Y3_use)
    total_needed = sum(heights) + (len(heights) - 1) * GROUP_GAP

    # Centra il blocco nell'area disponibile
    center_y = (avail_top + avail_bot) / 2
    # current_top = y del bordo superiore del primo nodo
    current_top = center_y + total_needed / 2

    for gi, (det, (bu_mid_y, bu_bg, bu_acc)) in enumerate(zip(bu_details, bu_mids)):
        for i, (lbl, sub) in enumerate(det):
            node_bot = current_top - NH_L3
            draw_node(pdf, col_x, node_bot, NW, NH_L3, lbl, sub,
                      bg=DARK3, accent=bu_acc, small=True)
            node_mid = node_bot + NH_L3 / 2
            draw_conn(pdf, col_x - GAP_X, bu_mid_y, col_x, node_mid)
            current_top -= (NH_L3 + GAP_Y3_use)

        current_top -= (GROUP_GAP - GAP_Y3_use)   # gap extra tra gruppi


# ── Pagina principale ─────────────────────────────────────────────────────────
def build_page(pdf):
    c = pdf.c

    # Sfondo
    pdf.fill(DARK); c.rect(0, 0, W, H, fill=1, stroke=0)
    pdf.fill(HexColor("#1E2416"))
    c.rect(W*0.55, H*0.35, W*0.45, H*0.65, fill=1, stroke=0)

    # ── Header ────────────────────────────────────────────────────────────────
    pdf.fill(DARK2); c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    pdf.fill(GREEN);  c.rect(0, H - 3, W, 3, fill=1, stroke=0)

    pdf.text("EETRA  |  Alberatura Sito Web  2026",
             MARGIN, H - 18*mm, size=16, bold=True, color=OFF_WHITE)
    pdf.text("Struttura completa delle pagine del sito  ·  eetra.it",
             MARGIN, H - 25*mm, size=8, color=MUTED_LT)
    pdf.text(datetime.now().strftime("Generato il %d/%m/%Y"),
             W - MARGIN, H - 18*mm, size=7.5, color=MUTED_LT, align="right")

    # ── Legenda (in riga, passo fisso 175pt) ──────────────────────────────────
    legend_items = [
        (COLOR_CORE,   "Sezioni core"),
        (COLOR_IMPACT, "Impact / Blog"),
        (COLOR_GOV,    "Governance"),
        (COLOR_WHY,    "Contatti"),
    ]
    lx0 = W - MARGIN - 3 * 175 - 120   # ancora a destra del titolo data
    ly  = H - 18*mm
    pdf.text("LEGENDA:", lx0 - 58, ly - 2, size=6.5, bold=True, color=MUTED_LT)
    for i, (col, lbl) in enumerate(legend_items):
        lxi = lx0 + i * 175
        pdf.fill(col); c.roundRect(lxi, ly - 8, 8, 8, 2, fill=1, stroke=0)
        pdf.text(lbl, lxi + 11, ly - 2, size=6.5, color=MUTED_LT)

    # Separatore
    pdf.stroke(HexColor("#2E3320"), 0.6)
    c.line(MARGIN, H - HEADER_H - 1, W - MARGIN, H - HEADER_H - 1)

    # ── HOME (COL0) ────────────────────────────────────────────────────────────
    home_mid_y = (TREE_TOP + TREE_BOT) / 2
    home_bot   = home_mid_y - NH_BIG / 2
    draw_node(pdf, COL0, home_bot, NW, NH_BIG,
              "Consulenza ESG", "per Aziende e PMI",
              bg=DARK3, accent=GREEN_HOVER)
    home_mid_y = home_bot + NH_BIG / 2

    # ── L1 (COL1) ─────────────────────────────────────────────────────────────
    pages_l1 = [
        ("Chi Siamo",   "Società Benefit · B Corp",   COLOR_CORE,   GREEN_PALE),
        ("Servizi ESG", "4 Business Unit",             COLOR_CORE,   GREEN_PALE),
        ("Impact",      "Blog ESG · News",             COLOR_IMPACT, HexColor("#7EC8A4")),
        ("Governance",  "Relazioni · Report · B Corp", COLOR_GOV,    HexColor("#7BB8D4")),
        ("Contatti",    "CTA Consulenza",              COLOR_WHY,    HexColor("#D4A84B")),
    ]
    n_l1 = len(pages_l1)
    total_l1 = n_l1 * NH + (n_l1 - 1) * GAP_L1
    start_l1  = home_mid_y + total_l1 / 2 - NH

    l1_mids = []
    for i, (lbl, sub, bg, acc) in enumerate(pages_l1):
        yb = start_l1 - i * (NH + GAP_L1)
        draw_node(pdf, COL1, yb, NW, NH, lbl, sub, bg=bg, accent=acc)
        mid = yb + NH / 2
        l1_mids.append((mid, bg, acc))
        draw_conn(pdf, COL0 + NW, home_mid_y, COL1, mid)

    # ── L2 Chi Siamo (COL2) ───────────────────────────────────────────────────
    draw_l2(pdf, COL2, l1_mids[0][0],
            [("Mission & Visione ESG",      ""),
             ("Team Esperti LEED · WELL",   ""),
             ("Certificazione B Corp 86,7", ""),
             ("Partnership Strategiche",    "Aziendali"),
             ("Partnership Istituzionali",  "Enti · Università")],
            COLOR_CORE, GREEN_PALE)

    # ── L2 Servizi — 4 BU (COL2) ──────────────────────────────────────────────
    serv_l2_mids = draw_l2(pdf, COL2, l1_mids[1][0],
            [("Company Atlas",              "ESG aziendale"),
             ("Positive Impact",            "Prodotti · LCA · EPD"),
             ("Environmental Intelligence", "Edifici · LEED · BREEAM"),
             ("Innovation Engine",          "AI · Data · Strumenti")],
            COLOR_CORE, GREEN_PALE, return_mids=True)

    # ── L2 Impact (COL2) ──────────────────────────────────────────────────────
    draw_l2(pdf, COL2, l1_mids[2][0],
            [("Aggiornamenti CSRD 2025",  "Notizie normative"),
             ("Case Study ESG Italiane",  "Storie d'impatto"),
             ("Guida Carbon Footprint",   "Scope 1 2 3"),
             ("Archivio per categoria",   "ESG · Cert · Norm.")],
            COLOR_IMPACT, HexColor("#7EC8A4"))

    # ── L2 Governance (COL2) ──────────────────────────────────────────────────
    draw_l2(pdf, COL2, l1_mids[3][0],
            [("Relazione d'Impatto PDF",  "Download annuale"),
             ("Impact Report B Corp",     "Punteggio 86,7"),
             ("Archivio report per anno", ""),
             ("Modello di Governance",    "Società Benefit")],
            COLOR_GOV, HexColor("#7BB8D4"))

    # ── L3 Servizi — layout SEQUENZIALE (COL3) ────────────────────────────────
    bu_details = [
        # Company Atlas (6 voci)
        [("ESG Reporting CSRD/ESRS",   "VSME"),
         ("Carbon Footprint Scope 1-3","GHG Protocol"),
         ("Bilancio di Sostenibilità", ""),
         ("Certificazione B Corp",     ""),
         ("Tassonomia UE · DNSH",      ""),
         ("Fractional ESG Manager",    "")],
        # Positive Impact (5 voci)
        [("LCA Carbon Footprint Pdto", "ISO 14044"),
         ("EPD · HPD · Declare",       ""),
         ("Cradle to Cradle C2C",      ""),
         ("Conformità CAM",            "Appalti pubblici"),
         ("Supporto CBAM",             "Carbon Border")],
        # Environmental Intelligence (6 voci)
        [("Certificazione LEED",       "BD+C ID+C"),
         ("Certificazione BREEAM",     "Assessor Italia"),
         ("Certificazione WELL",       "Benessere uffici"),
         ("GRESB Real Estate",         "Rating ESG"),
         ("CRREM Energy Modeling",     "Decarbonizzazione"),
         ("Tassonomia UE DNSH",        "Immobiliare")],
        # Innovation Engine (4 voci)
        [("ARIA Air Quality",          "Qualità aria"),
         ("EETRA Material Library",    "Database ESG"),
         ("Carbon Digital Twin",       "Whole Life Carbon"),
         ("TIAKI Logistics",           "Supply chain")],
    ]

    draw_l3_sequential(pdf, COL3, serv_l2_mids, bu_details,
                       avail_top=TREE_TOP, avail_bot=TREE_BOT)

    # ── Footer ────────────────────────────────────────────────────────────────
    pdf.fill(DARK2); c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    pdf.stroke(GREEN, 0.4); c.line(0, FOOTER_H, W, FOOTER_H)
    pdf.text("EETRA Srl SB  ·  Via Plinio 43, Milano  ·  info@eetra.it  ·  +39 02 25565011  ·  www.eetra.it",
             W/2, FOOTER_H - 8*mm, size=7, color=MUTED_LT, align="center")
    pdf.text("© 2026 EETRA  ·  Tutti i diritti riservati",
             W/2, FOOTER_H - 12*mm, size=6, color=MUTED_DK, align="center")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pdf = PDF(OUT)
    build_page(pdf)
    pdf.save()
    print(f"Apri: {OUT}")

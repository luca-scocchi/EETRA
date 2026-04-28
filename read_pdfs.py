import PyPDF2
import os

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    files = [
        r"c:\Users\Utente\Desktop\Sito Eetra\infosito\eetra_sitemap_v4.pdf",
        r"c:\Users\Utente\Desktop\Sito Eetra\infosito\eetra_seo_sitemap.pdf",
        r"c:\Users\Utente\Desktop\Sito Eetra\infosito\05_Company Profile\EETRA_CompanyProfile__Palette_Fonts_Colori.pdf"
    ]
    with open("pdf_contents.txt", "w", encoding="utf-8") as out:
        for f in files:
            out.write(f"--- {os.path.basename(f)} ---\n")
            out.write(read_pdf(f) + "\n\n")

# Relazioni d'Impatto EETRA — Cartella PDF

Questa cartella contiene i file PDF delle Relazioni d'Impatto annuali di EETRA Srl SB.

## Come aggiungere un nuovo report

1. Salva il PDF in questa cartella con il nome: `relazione-impatto-ANNO.pdf`
   Esempio: `relazione-impatto-2024.pdf`

2. Apri il file `relazioni-di-impatto.html`

3. Trova il blocco della card corrispondente all'anno

4. Aggiorna l'attributo `href` del link di download:
   ```html
   <a href="relazioni/relazione-impatto-2024.pdf" download ...>
   ```

5. Se vuoi anche mostrare la copertina del PDF come immagine:
   - Esporta la prima pagina del PDF come JPG
   - Salvala come `cover-ANNO.jpg` in questa cartella
   - Nella card, sostituisci l'elemento `cover-placeholder` con:
   ```html
   <img src="relazioni/cover-2024.jpg" alt="Relazione d'Impatto 2024">
   ```

## File presenti

- (aggiungi qui i PDF man mano che vengono caricati)

## Note

- I file PDF non devono superare i 25 MB per garantire un download fluido
- Formato consigliato: PDF/A per massima compatibilità
- Contatta info@eetra.it per supporto tecnico

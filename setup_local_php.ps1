# Script di configurazione server locale PHP per EETRA
$phpDir = "c:\Users\Utente\Desktop\Sito Eetra\.php_local"
$zipPath = "$phpDir\php.zip"

Write-Host "1. Creazione cartella .php_local..."
If (!(Test-Path $phpDir)) {
    New-Item -ItemType Directory -Path $phpDir -Force | Out-Null
}

Write-Host "2. Download di PHP 8.2.20 in corso..."
# Scarichiamo PHP 8.2.20 ufficiale per Windows
Invoke-WebRequest -Uri "https://windows.php.net/downloads/releases/archives/php-8.2.20-nts-Win32-vs16-x64.zip" -OutFile $zipPath

Write-Host "3. Estrazione dello zip..."
Expand-Archive -Path $zipPath -DestinationPath $phpDir -Force

Write-Host "4. Copia del file php.ini..."
if (Test-Path "$phpDir\php.ini-development") {
    Copy-Item "$phpDir\php.ini-development" "$phpDir\php.ini" -Force
}

# Modifichiamo php.ini per abilitare l'estensione gd, mbstring e impostare i limiti di upload
$iniPath = "$phpDir\php.ini"
(Get-Content $iniPath) | ForEach-Object {
    $_ -replace ';extension=gd', 'extension=gd' `
       -replace ';extension=mbstring', 'extension=mbstring' `
       -replace ';extension_dir = "ext"', 'extension_dir = "ext"' `
       -replace 'upload_max_filesize = 2M', 'upload_max_filesize = 20M' `
       -replace 'post_max_size = 8M', 'post_max_size = 25M'
} | Set-Content $iniPath

Write-Host "5. Arresto del server Python precedente sulla porta 8000..."
try {
    $processId = (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess
    if ($processId) {
        Stop-Process -Id $processId -Force
        Write-Host "   Server Python (PID $processId) arrestato."
    }
} catch {
    Write-Host "   Nessun server trovato sulla porta 8000."
}

Write-Host "6. Avvio del server locale PHP sulla porta 8000..."
# Avviamo il server PHP
Start-Process -NoNewWindow -FilePath "$phpDir\php.exe" -ArgumentList "-S", "localhost:8000", "-c", "$iniPath"

Write-Host "🎉 Server PHP avviato con successo su http://localhost:8000!"
Write-Host "Ora puoi aprire http://localhost:8000/gestione-sito.html e accedere digitando 'eetra2024'."

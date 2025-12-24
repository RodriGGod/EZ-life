# Script para compilar el instalador de EZLife Tool con Inno Setup
# Asegúrate de tener Inno Setup instalado en la ruta por defecto

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  EZLife Tool - Build Installer" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Ruta del compilador de Inno Setup
$iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

# Verificar si existe Inno Setup
if (-not (Test-Path $iscc)) {
    Write-Host "❌ Error: Inno Setup no encontrado en: $iscc" -ForegroundColor Red
    Write-Host "   Por favor, instala Inno Setup 6 desde: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    exit 1
}

# Verificar que existen los archivos .exe
$exeFiles = @(
    "src\dist\EZLife_Config.exe",
    "src\dist\controlador.exe",
    "src\dist\EZLife_Browser.exe"
)

$missing = @()
foreach ($file in $exeFiles) {
    if (-not (Test-Path $file)) {
        $missing += $file
    }
}

if ($missing.Count -gt 0) {
    Write-Host "❌ Error: Faltan archivos compilados:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
    Write-Host ""
    Write-Host "   Ejecuta primero los scripts .spec con PyInstaller" -ForegroundColor Yellow
    exit 1
}

# Compilar el instalador
Write-Host "🔨 Compilando instalador..." -ForegroundColor Green
& $iscc "setup_script.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Instalador compilado exitosamente!" -ForegroundColor Green
    Write-Host "📦 Ubicación: Output\EZLifeInstaller.exe" -ForegroundColor Cyan
    
    # Abrir la carpeta Output
    if (Test-Path "Output\EZLifeInstaller.exe") {
        $size = (Get-Item "Output\EZLifeInstaller.exe").Length / 1MB
        Write-Host "📊 Tamaño: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "¿Deseas abrir la carpeta Output? (S/N)" -ForegroundColor Yellow
        $response = Read-Host
        if ($response -eq "S" -or $response -eq "s") {
            explorer.exe "Output"
        }
    }
} else {
    Write-Host ""
    Write-Host "❌ Error al compilar el instalador" -ForegroundColor Red
    exit 1
}

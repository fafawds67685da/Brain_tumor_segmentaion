Write-Host "=====================================================" -ForegroundColor Green
Write-Host "  Brain Tumor Segmentation - Complete Setup & Start" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.9 or higher" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "🔍 Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "app.py",
    "backend.py",
    "requirements.txt",
    "unet_brain_tumor_final.keras"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (MISSING)" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Some required files are missing!" -ForegroundColor Red
    Write-Host "   Missing files: $($missingFiles -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit
    }
}

Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Error installing dependencies!" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "🚀 Starting Backend and Frontend..." -ForegroundColor Green
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Backend will start in this window" -ForegroundColor Cyan
Write-Host "  Frontend will open in a new browser tab" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {python backend.py}"

# Wait a bit for backend to start
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend in this window
Write-Host "✅ Backend started!" -ForegroundColor Green
Write-Host "🎨 Starting frontend..." -ForegroundColor Green
Write-Host ""

streamlit run app.py

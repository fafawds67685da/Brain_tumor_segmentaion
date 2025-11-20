Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Brain Tumor Segmentation - FastAPI Backend" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔍 Checking model file..." -ForegroundColor Yellow

if (Test-Path "unet_brain_tumor_final.keras") {
    Write-Host "✅ Model file found!" -ForegroundColor Green
} else {
    Write-Host "❌ Model file not found!" -ForegroundColor Red
    Write-Host "   Please ensure 'unet_brain_tumor_final.keras' is in the current directory" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "🚀 Starting FastAPI Backend Server..." -ForegroundColor Green
Write-Host "📍 API URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python backend.py

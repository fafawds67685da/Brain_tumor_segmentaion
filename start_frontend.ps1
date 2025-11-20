Write-Host "================================================" -ForegroundColor Magenta
Write-Host "  Brain Tumor Segmentation - Streamlit Dashboard" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "🔍 Checking Stats directory..." -ForegroundColor Yellow

if (Test-Path "Stats") {
    Write-Host "✅ Stats directory found!" -ForegroundColor Green
} else {
    Write-Host "❌ Stats directory not found!" -ForegroundColor Red
    Write-Host "   The dashboard may not display all visualizations" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎨 Starting Streamlit Dashboard..." -ForegroundColor Green
Write-Host "📍 Dashboard URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Make sure the FastAPI backend is running on port 8000" -ForegroundColor Yellow
Write-Host "   Run 'start_backend.ps1' in another terminal if not started" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the dashboard" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

# 🚀 Quick Start Guide

## For Windows Users

### Option 1: Automatic Setup (Recommended)

1. **Open PowerShell in the project directory**
   ```powershell
   cd d:\Brain_tumor_segmentaion
   ```

2. **Run the all-in-one startup script**
   ```powershell
   .\start_all.ps1
   ```
   
   This will:
   - Check Python installation
   - Verify all required files
   - Install dependencies
   - Start both backend and frontend

### Option 2: Manual Setup

1. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Start Backend (Terminal 1)**
   ```powershell
   .\start_backend.ps1
   ```
   Or manually:
   ```powershell
   python backend.py
   ```

3. **Start Frontend (Terminal 2)**
   ```powershell
   .\start_frontend.ps1
   ```
   Or manually:
   ```powershell
   streamlit run app.py
   ```

### Option 3: Testing the API

After starting the backend, test it:
```powershell
python test_api.py
```

## 📍 Access Points

- **Streamlit Dashboard**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## ⚠️ Troubleshooting

### PowerShell Execution Policy Error
If you get an error running .ps1 scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use
If port 8000 or 8501 is already in use:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Model Not Loading
Ensure the model file exists:
```powershell
dir unet_brain_tumor_final.keras
```

### Import Errors
Reinstall dependencies:
```powershell
pip install -r requirements.txt --upgrade --force-reinstall
```

## 🎯 Quick Test

1. Start backend
2. Open http://localhost:8000/health in browser
3. Should see: `{"status": "healthy", "model_loaded": true, ...}`

## 📊 Features to Try

1. **Overview Page**: See project summary and dataset split
2. **Dataset Statistics**: Explore interactive visualizations
3. **Training Results**: View training curves and metrics
4. **Model Testing**: Upload images or use test images for segmentation

## 🔧 Configuration

### Change API Port
Edit `backend.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to desired port
```

### Change Frontend API URL
Edit `app.py`:
```python
API_URL = "http://localhost:8000"  # Update with your backend URL
```

## 📝 Notes

- The frontend needs the backend to be running for the "Model Testing" feature
- Other pages (statistics, visualizations) work independently
- Test images are in the `Test_images/` folder
- All HTML visualizations are interactive (Plotly)

## 🆘 Getting Help

1. Check the full README.md for detailed documentation
2. Review error messages in the terminal
3. Check API logs for backend issues
4. Verify all required files are present

## ✅ Verification Checklist

Before starting, verify:
- [ ] Python 3.9+ installed
- [ ] All files present (app.py, backend.py, requirements.txt, model file)
- [ ] Dependencies installed
- [ ] Stats/ folder present with all subdirectories
- [ ] Test_images/ folder present with images
- [ ] Ports 8000 and 8501 available

---

**Ready to go? Run `.\start_all.ps1` and enjoy! 🎉**

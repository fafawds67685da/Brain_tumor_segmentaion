# Brain Tumor Segmentation — Backend + Streamlit Frontend

This workspace contains a FastAPI backend (`backend.py`) that loads a U-Net brain tumor segmentation model (`unet_brain_tumor_final.keras`) and exposes prediction endpoints, plus a Streamlit frontend (`streamlit_app.py`) to preview the `Stats/` HTML reports and run model inference on images in `Test_images/`.

---

## 🚀 Key Features (Updated)

- **Streamlit frontend (`streamlit_app.py`)**
  - Multi-page dashboard with sidebar navigation
  - Interactive visualization of all statistics in `Stats/` (HTML, JSON)
  - Paginated tables for large JSON stats (cap 2 and cap 4), with correct row indices
  - Dynamic captions parsed from `caption.txt` files and shown under graphs (except cap 3 and cap 6)
  - JSON stats displayed in a readable format
  - Model prediction page: upload/select images, view segmentation results

- **FastAPI backend (`backend.py`)**
  - RESTful API for tumor segmentation
  - Single and batch prediction endpoints
  - Serves static stats files from `Stats/`

---

## 🛠️ Quick Start

1. Create a Python virtual environment and activate it.
   ```powershell
   python -m venv .venv; .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Start the backend:
   ```powershell
   uvicorn backend:app --reload
   # or
   python backend.py
   ```
3. Start the Streamlit frontend:
   ```powershell
   streamlit run streamlit_app.py
   ```

---

## 📝 Notes
- The dashboard now supports paginated tables for large stats (cap 2 and cap 4), with correct row indices.
- Captions are dynamically parsed and shown under graphs, except for cap 3 and cap 6.
- Sidebar navigation and multi-page layout are implemented.
- JSON stats are displayed in a readable format.
- The model expects grayscale MRI images, resized to 128x128 for prediction.

For more details, see the full documentation below.

# 🧠 Brain Tumor Segmentation Dashboard

A comprehensive web application for brain tumor segmentation using U-Net deep learning model. This project includes a **Streamlit frontend** for interactive visualization and a **FastAPI backend** for real-time model predictions.

## 📋 Features

### Frontend (Streamlit)
- 📊 **Interactive Dashboard** with multiple analysis sections
- 📈 **Dataset Statistics** visualization
- 🔬 **Slice-level Analysis** of MRI scans
- 🔄 **Data Augmentation** insights
- 📉 **Training Results** with interactive plots
- 🧪 **Model Testing** interface for new images

### Backend (FastAPI)
- 🚀 **RESTful API** for tumor segmentation
- 🔍 **Single and Batch Prediction** endpoints
- 🎯 **Real-time Segmentation** with U-Net model
- 📊 **Automatic Metrics** calculation
- 🖼️ **Image Overlay** visualization

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to the project directory**
```powershell
cd d:\Brain_tumor_segmentaion
```

2. **Create a virtual environment (recommended)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Verify model file exists**
Ensure `unet_brain_tumor_final.keras` is in the project root directory.

## 🚀 Running the Application

### Method 1: Run Backend and Frontend Separately

#### Terminal 1 - Start FastAPI Backend:
```powershell
python backend.py
```
The API will be available at:
- Main API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

#### Terminal 2 - Start Streamlit Frontend:
```powershell
streamlit run app.py
```
The dashboard will open automatically at: http://localhost:8501

### Method 2: Using Scripts (Create these if needed)

**start_backend.ps1**
```powershell
Write-Host "🚀 Starting FastAPI Backend..." -ForegroundColor Green
python backend.py
```

**start_frontend.ps1**
```powershell
Write-Host "🎨 Starting Streamlit Frontend..." -ForegroundColor Cyan
streamlit run app.py
```

## 📖 API Documentation

### Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

#### 2. Health Check
```
GET /health
```
Check if the API and model are loaded correctly.

#### 3. Model Information
```
GET /model-info
```
Get details about the loaded U-Net model.

#### 4. Single Image Prediction
```
POST /predict
```
**Parameters:**
- `file`: Image file (PNG, JPG, JPEG)

**Response:**
```json
{
  "success": true,
  "tumor_pixels": 1234,
  "total_pixels": 16384,
  "tumor_percentage": 7.53,
  "segmented_image": "base64_encoded_image",
  "mask": "base64_encoded_mask",
  "original_size": [256, 256],
  "model_size": [128, 128]
}
```

#### 5. Batch Prediction
```
POST /batch-predict
```
**Parameters:**
- `files`: List of image files (max 10)

**Response:**
```json
{
  "total_images": 5,
  "successful": 5,
  "failed": 0,
  "results": [...]
}
```

## 🎨 Frontend Pages

### 1. Overview
- Project summary
- Dataset information
- Model architecture details

### 2. Dataset Statistics
- 3D volume distribution
- Tumor distribution analysis
- Intensity statistics
- Tumor percentage distribution

### 3. Slice-Level Analysis
- Tumor pixel distribution
- Mean intensity analysis
- Standard deviation patterns
- Correlation matrix

### 4. Data Augmentation
- Augmentation examples
- Intensity shift analysis
- Augmentation statistics

### 5. Training Results
- Loss curves
- Accuracy curves
- Dice coefficient progression
- Complete training history

### 6. Model Testing
- Upload custom MRI images
- Select from test images
- Real-time segmentation
- Tumor metrics display

## 🧪 Testing the Application

### Using cURL (API Testing)

```powershell
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model-info

# Predict (with test image)
curl -X POST "http://localhost:8000/predict" -F "file=@Test_images/raw_mri_1.png"
```

### Using Python

```python
import requests

# Test prediction
url = "http://localhost:8000/predict"
files = {'file': open('Test_images/raw_mri_1.png', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

## 📁 Project Structure

```
Brain_tumor_segmentaion/
├── app.py                              # Streamlit frontend
├── backend.py                          # FastAPI backend
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── unet_brain_tumor_final.keras       # Trained U-Net model
├── Stats/                             # Statistics and visualizations
│   ├── cap 2/                        # Dataset statistics
│   ├── cap 3/                        # Dataset split info
│   ├── cap 4/                        # Slice-level analysis
│   ├── cap 5/                        # Augmentation analysis
│   └── cap 6/                        # Training results
└── Test_images/                       # Test MRI images
    ├── raw_mri_1.png
    ├── raw_mri_2.png
    ├── raw_mri_3.png
    ├── raw_mri_4.png
    └── raw_mri_5.png
```

## 🔧 Configuration

### Backend Configuration
Edit `backend.py` to change:
- `MODEL_PATH`: Path to the model file
- Port number in `uvicorn.run()`

### Frontend Configuration
Edit `app.py` to change:
- `API_URL`: Backend API URL (default: http://localhost:8000)
- Page layout and styling

## 📊 Model Information

- **Architecture**: U-Net 2D
- **Input Size**: 128x128x1 (grayscale)
- **Output**: 128x128x1 (binary mask)
- **Task**: Binary segmentation (tumor vs background)
- **Dataset**: BraTS 2020
- **Training Split**: 18,265 train / 3,653 val / 2,436 test

### Performance Metrics (Final Epoch)
- **Validation Loss**: 0.0057
- **Validation Accuracy**: 99.77%
- **Validation Dice Score**: 0.9427

## 🐛 Troubleshooting

### Model Not Loading
- Verify `unet_brain_tumor_final.keras` exists in the project root
- Check Python and TensorFlow versions are compatible

### API Connection Error
- Ensure backend is running on port 8000
- Check firewall settings
- Verify `API_URL` in `app.py` is correct

### Import Errors
- Reinstall requirements: `pip install -r requirements.txt --upgrade`
- Check Python version compatibility

### Streamlit Issues
- Clear cache: Delete `.streamlit` folder
- Restart Streamlit server

## 📝 Notes

- The model expects grayscale MRI images
- Images are automatically resized to 128x128 for prediction
- Output images are resized back to original dimensions
- Tumor regions are highlighted in red with green contours

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Add new visualizations

## 📄 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- BraTS 2020 Dataset
- TensorFlow/Keras team
- Streamlit team
- FastAPI team

---

**Built with ❤️ using TensorFlow, FastAPI, and Streamlit**

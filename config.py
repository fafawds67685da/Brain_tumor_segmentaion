# Configuration File for Brain Tumor Segmentation Application

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 1

# Model Configuration
MODEL_PATH = "unet_brain_tumor_final.keras"
MODEL_INPUT_SIZE = (128, 128)
PREDICTION_THRESHOLD = 0.5

# Image Processing
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
MAX_BATCH_SIZE = 10
IMAGE_NORMALIZATION = True

# Streamlit Configuration
STREAMLIT_PORT = 8501
STREAMLIT_THEME = "light"

# Paths
STATS_DIR = "Stats"
TEST_IMAGES_DIR = "Test_images"

# Visualization
TUMOR_COLOR = (255, 0, 0)  # Red
CONTOUR_COLOR = (0, 255, 0)  # Green
OVERLAY_ALPHA = 0.3

# Performance
ENABLE_GPU = True
TF_MEMORY_GROWTH = True

# Logging
LOG_LEVEL = "INFO"
SAVE_PREDICTIONS = False
PREDICTION_SAVE_DIR = "predictions"

# Security
MAX_FILE_SIZE_MB = 10
CORS_ORIGINS = ["*"]

# Dashboard
SHOW_RAW_JSON = True
ENABLE_FILE_UPLOAD = True
ENABLE_BATCH_PROCESSING = True

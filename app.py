import streamlit as st
import plotly.io as pio
import json
from pathlib import Path
import requests
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Brain Tumor Segmentation Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        margin-top: 30px;
        margin-bottom: 20px;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    .caption-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = "http://localhost:8000"

def load_html_file(file_path):
    """Load and return HTML file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def load_json_file(file_path):
    """Load and return JSON file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def load_caption(file_path):
    """Load caption text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Caption not available"

# Main header
st.markdown('<h1 class="main-header">🧠 Brain Tumor Segmentation Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Section",
    ["Overview", "Dataset Statistics", "Slice-Level Analysis", "Data Augmentation", 
     "Training Results", "Model Testing"]
)

# Overview Page
if page == "Overview":
    st.markdown('<h2 class="section-header">Project Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>📁 Dataset</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #667eea;">BraTS 2020</p>
            <p>Brain Tumor Segmentation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3>🏗️ Model</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #764ba2;">U-Net</p>
            <p>2D Convolutional Neural Network</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <h3>🎯 Task</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #667eea;">Binary Segmentation</p>
            <p>Tumor vs Background</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📝 Dataset Split")
    caption_3 = load_caption("Stats/cap 3/caption.txt")
    st.markdown(f'<div class="caption-box">{caption_3}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔍 About This Project")
    st.info("""
    This dashboard showcases a comprehensive brain tumor segmentation system using U-Net architecture.
    The system processes MRI scans from the BraTS 2020 dataset and provides accurate tumor segmentation.
    
    **Key Features:**
    - Interactive visualization of dataset statistics
    - Detailed analysis of MRI intensity distributions
    - Data augmentation strategies
    - Training performance metrics
    - Real-time model testing on new images
    """)

# Dataset Statistics Page
elif page == "Dataset Statistics":
    st.markdown('<h2 class="section-header">📊 Dataset Statistics</h2>', unsafe_allow_html=True)
    
    # Caption 1 - 3D Volumes
    st.markdown("### 🧊 3D Volume Distribution")
    caption_1 = load_caption("Stats/cap 2/cap 1/caption.txt")
    
    tab1, tab2 = st.tabs(["📈 3D Volumes", "🧩 Tumor Distribution"])
    
    with tab1:
        html_content = load_html_file("Stats/cap 2/cap 1/dataset_3d_volumes.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab2:
        html_content = load_html_file("Stats/cap 2/cap 1/dataset_tumor_distribution.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    st.markdown("---")
    
    # Caption 2 - Intensity and Tumor Stats
    st.markdown("### 📊 Intensity and Tumor Statistics")
    caption_2 = load_caption("Stats/cap 2/caption.txt")
    st.markdown(f'<div class="caption-box">{caption_2}</div>', unsafe_allow_html=True)
    
    tab3, tab4 = st.tabs(["📉 Tumor Percentage Distribution", "📊 Intensity Statistics"])
    
    with tab3:
        html_content = load_html_file("Stats/cap 2/tumor_percentage_distribution.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab4:
        html_content = load_html_file("Stats/cap 2/intensity_statistics_boxplots.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    # JSON Stats
    st.markdown("### 📋 Raw Statistics")
    json_data = load_json_file("Stats/cap 2/dataset_intensity_and_tumor_stats.json")
    if json_data:
        st.json(json_data)

# Slice-Level Analysis Page
elif page == "Slice-Level Analysis":
    st.markdown('<h2 class="section-header">🔬 Slice-Level Analysis</h2>', unsafe_allow_html=True)
    
    caption_4 = load_caption("Stats/cap 4/caption.txt")
    st.markdown(f'<div class="caption-box">{caption_4}</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Tumor Pixel Distribution",
        "💡 Mean Intensity",
        "📐 Std Intensity",
        "🔗 Correlation Matrix"
    ])
    
    with tab1:
        st.markdown("#### Tumor Pixel Distribution")
        html_content = load_html_file("Stats/cap 4/slice_tumor_pixel_distribution.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab2:
        st.markdown("#### Mean Intensity Distribution")
        html_content = load_html_file("Stats/cap 4/slice_mean_intensity_distribution.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab3:
        st.markdown("#### Intensity Standard Deviation")
        html_content = load_html_file("Stats/cap 4/slice_std_intensity_distribution.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab4:
        st.markdown("#### Slice Feature Correlation Heatmap")
        html_content = load_html_file("Stats/cap 4/slice_correlation_matrix.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    # JSON Stats
    st.markdown("### 📋 Slice-Level Statistics (JSON)")
    json_data = load_json_file("Stats/cap 4/slice_level_statistics.json")
    if json_data:
        with st.expander("View Raw Statistics"):
            st.json(json_data)

# Data Augmentation Page
elif page == "Data Augmentation":
    st.markdown('<h2 class="section-header">🔄 Data Augmentation Analysis</h2>', unsafe_allow_html=True)
    
    caption_5 = load_caption("Stats/cap 5/caption.txt")
    st.markdown(f'<div class="caption-box">{caption_5}</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🖼️ Augmentation Examples", "📊 Intensity Shift Analysis"])
    
    with tab1:
        st.markdown("#### Augmentation Examples")
        st.info("Random flips, rotations, and zoom operations applied to MRI slices")
        html_content = load_html_file("Stats/cap 5/augmentation_examples.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab2:
        st.markdown("#### Mean Intensity Shift")
        st.info("Effect of augmentation on pixel brightness distribution")
        html_content = load_html_file("Stats/cap 5/augmentation_mean_intensity_shift.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    # JSON Stats
    st.markdown("### 📋 Augmentation Statistics")
    json_data = load_json_file("Stats/cap 5/augmentation_stats.json")
    if json_data:
        st.json(json_data)

# Training Results Page
elif page == "Training Results":
    st.markdown('<h2 class="section-header">📈 Training Results</h2>', unsafe_allow_html=True)
    
    # Load training history
    training_data = load_json_file("Stats/cap 6/training_history.json")
    
    if training_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            final_loss = training_data['val_loss'][-1]
            st.metric("Final Val Loss", f"{final_loss:.6f}")
        
        with col2:
            final_acc = training_data['val_acc'][-1]
            st.metric("Final Val Accuracy", f"{final_acc:.4%}")
        
        with col3:
            final_dice = training_data['val_dice'][-1]
            st.metric("Final Val Dice Score", f"{final_dice:.4f}")
        
        with col4:
            epochs = len(training_data['epochs'])
            st.metric("Total Epochs", epochs)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📉 Loss Curves", "✅ Accuracy Curves", "🎯 Dice Score Curves"])
    
    with tab1:
        st.markdown("#### Training & Validation Loss")
        html_content = load_html_file("Stats/cap 6/training_loss_curve.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab2:
        st.markdown("#### Training & Validation Accuracy")
        html_content = load_html_file("Stats/cap 6/training_accuracy_curve.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    with tab3:
        st.markdown("#### Training & Validation Dice Coefficient")
        html_content = load_html_file("Stats/cap 6/training_dice_curve.html")
        if html_content:
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    # Training history JSON
    st.markdown("### 📋 Complete Training History")
    if training_data:
        with st.expander("View Raw Training Data"):
            st.json(training_data)

# Model Testing Page
elif page == "Model Testing":
    st.markdown('<h2 class="section-header">🧪 Model Testing</h2>', unsafe_allow_html=True)
    
    st.info("""
    Upload MRI images or select from test images to see the model's segmentation results.
    The U-Net model will identify tumor regions in the brain MRI scans.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Upload Image")
        uploaded_file = st.file_uploader("Choose an MRI image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded MRI Image', use_column_width=True)
            
            if st.button("🔍 Run Segmentation", key="upload_btn"):
                with st.spinner("Running segmentation..."):
                    try:
                        # Convert image to bytes
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        # Send to API
                        files = {'file': ('image.png', img_bytes, 'image/png')}
                        response = requests.post(f"{API_URL}/predict", files=files)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            with col2:
                                st.markdown("### 🎯 Segmentation Result")
                                
                                # Display segmented image
                                segmented_img_data = base64.b64decode(result['segmented_image'])
                                segmented_img = Image.open(io.BytesIO(segmented_img_data))
                                st.image(segmented_img, caption='Segmented Image', use_column_width=True)
                                
                                # Display metrics
                                st.markdown("#### 📊 Prediction Metrics")
                                metric_col1, metric_col2 = st.columns(2)
                                with metric_col1:
                                    st.metric("Tumor Pixels", result['tumor_pixels'])
                                with metric_col2:
                                    st.metric("Tumor Percentage", f"{result['tumor_percentage']:.2f}%")
                                
                                st.success("✅ Segmentation completed successfully!")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Please ensure the FastAPI backend is running on port 8000.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("### 🖼️ Or Select Test Image")
        
        # List test images
        test_images_dir = Path("Test_images")
        if test_images_dir.exists():
            test_images = list(test_images_dir.glob("*.png"))
            if test_images:
                selected_image = st.selectbox(
                    "Select a test image",
                    options=[img.name for img in test_images]
                )
                
                if selected_image:
                    test_image_path = test_images_dir / selected_image
                    image = Image.open(test_image_path)
                    st.image(image, caption=f'Test Image: {selected_image}', use_column_width=True)
                    
                    if st.button("🔍 Run Segmentation on Test Image", key="test_btn"):
                        with st.spinner("Running segmentation..."):
                            try:
                                # Read image and send to API
                                with open(test_image_path, 'rb') as f:
                                    files = {'file': (selected_image, f, 'image/png')}
                                    response = requests.post(f"{API_URL}/predict", files=files)
                                
                                if response.status_code == 200:
                                    result = response.json()
                                    
                                    st.markdown("### 🎯 Segmentation Result")
                                    
                                    # Display segmented image
                                    segmented_img_data = base64.b64decode(result['segmented_image'])
                                    segmented_img = Image.open(io.BytesIO(segmented_img_data))
                                    st.image(segmented_img, caption='Segmented Image', use_column_width=True)
                                    
                                    # Display metrics
                                    st.markdown("#### 📊 Prediction Metrics")
                                    metric_col1, metric_col2 = st.columns(2)
                                    with metric_col1:
                                        st.metric("Tumor Pixels", result['tumor_pixels'])
                                    with metric_col2:
                                        st.metric("Tumor Percentage", f"{result['tumor_percentage']:.2f}%")
                                    
                                    st.success("✅ Segmentation completed successfully!")
                                else:
                                    st.error(f"Error: {response.json()['detail']}")
                            except requests.exceptions.ConnectionError:
                                st.error("❌ Cannot connect to API. Please ensure the FastAPI backend is running on port 8000.")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("No test images found in Test_images directory")
        else:
            st.warning("Test_images directory not found")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🧠 Brain Tumor Segmentation Dashboard | Built with Streamlit & FastAPI</p>
        <p>Model: U-Net | Dataset: BraTS 2020</p>
    </div>
""", unsafe_allow_html=True)

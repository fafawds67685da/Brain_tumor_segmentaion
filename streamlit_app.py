import streamlit as st
from pathlib import Path
import requests
import base64
import io
import json
import mimetypes
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
STATS_DIR = ROOT / "Stats"
TEST_IMAGES_DIR = ROOT / "Test_images"

st.set_page_config(page_title="Brain Tumor Segmentation", layout="wide", initial_sidebar_state="expanded")

# Folder metadata with headings
FOLDER_INFO = {
    "cap 2/cap 1": {
        "heading": "📊 Dataset Overview",
        "description": "Tumor distribution and 3D MRI volumes analysis"
    },
    "cap 2": {
        "heading": "📈 Tumor & Intensity Statistics", 
        "description": "Tumor percentage distribution and MRI intensity statistics"
    },
    "cap 3": {
        "heading": "📦 Dataset Split Summary",
        "description": "Train, validation, and test set sizes"
    },
    "cap 4": {
        "heading": "🔬 Slice-Level Analysis",
        "description": "Tumor pixels, intensity distribution, and feature correlations"
    },
    "cap 5": {
        "heading": "🎨 Data Augmentation",
        "description": "Augmentation examples and intensity shift analysis"
    },
    "cap 6": {
        "heading": "📉 Training Metrics",
        "description": "Loss, accuracy, and dice coefficient curves"
    }
}

# Backend URL
if 'backend_url' not in st.session_state:
    st.session_state.backend_url = "http://localhost:8000"

# Navigation
st.sidebar.title("🧠 Brain Tumor Segmentation")
page = st.sidebar.radio("Navigate", ["📊 Statistics", "🔮 Prediction"])

st.sidebar.markdown("---")
st.sidebar.caption("Backend Configuration")
backend_url = st.sidebar.text_input("Backend URL", value=st.session_state.backend_url, key="backend_input")
st.session_state.backend_url = backend_url


# ==================== STATISTICS PAGE ====================
if page == "📊 Statistics":
    st.title("📊 Dataset & Training Statistics")
    st.markdown("Explore comprehensive statistics and visualizations from the brain tumor segmentation project.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Select Statistics Category")
    
    # Get available folders
    available_folders = []
    if STATS_DIR.exists():
        for folder_key in FOLDER_INFO.keys():
            folder_path = STATS_DIR / folder_key
            if folder_path.exists():
                available_folders.append(folder_key)
    
    if not available_folders:
        st.warning("No statistics folders found!")
    else:
        # Folder selection
        selected_folder = st.sidebar.selectbox(
            "Choose category:",
            options=available_folders,
            format_func=lambda x: FOLDER_INFO[x]["heading"]
        )
        
        folder_path = STATS_DIR / selected_folder
        folder_meta = FOLDER_INFO[selected_folder]
        
        # Display folder heading and description
        st.header(folder_meta["heading"])
        st.markdown(f"*{folder_meta['description']}*")
        st.markdown("---")
        
        # Read caption if exists
        caption_file = folder_path / "caption.txt"
        if caption_file.exists():
            caption_text = caption_file.read_text(encoding='utf-8', errors='ignore')
            with st.expander("📝 About this section", expanded=True):
                st.markdown(caption_text)
        
        # Get all HTML and JSON files in the folder
        html_files = sorted(folder_path.glob("*.html"))
        json_files = sorted(folder_path.glob("*.json"))
        
        # Display HTML visualizations
        if html_files:
            st.subheader("📊 Visualizations")
            for html_file in html_files:
                st.markdown(f"### {html_file.stem.replace('_', ' ').title()}")
                
                # Try to load via backend first, fallback to local
                served_url = f"{backend_url}/stats/{html_file.relative_to(STATS_DIR).as_posix()}"
                try:
                    components.iframe(served_url, height=600, scrolling=True)
                except Exception:
                    html_content = html_file.read_text(encoding='utf-8', errors='ignore')
                    components.html(html_content, height=600, scrolling=True)
                
                st.markdown("---")
        
        # Display JSON data
        if json_files:
            st.subheader("📋 Numerical Statistics")
            for json_file in json_files:
                with st.expander(f"📄 {json_file.stem.replace('_', ' ').title()}", expanded=False):
                    try:
                        data = json.loads(json_file.read_text(encoding='utf-8'))
                        
                        # Special handling for training history
                        if "epochs" in data and "train_loss" in data:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Epochs", len(data["epochs"]))
                            with col2:
                                st.metric("Final Train Loss", f"{data['train_loss'][-1]:.6f}")
                            with col3:
                                st.metric("Final Val Loss", f"{data['val_loss'][-1]:.6f}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Final Train Dice", f"{data['train_dice'][-1]:.4f}")
                            with col2:
                                st.metric("Final Val Dice", f"{data['val_dice'][-1]:.4f}")
                        
                        # Show raw JSON in expandable section
                        with st.expander("Show raw data"):
                            st.json(data)
                    except Exception as e:
                        st.error(f"Error loading JSON: {e}")


# ==================== PREDICTION PAGE ====================
elif page == "🔮 Prediction":
    st.title("🔮 Brain Tumor Segmentation Prediction")
    st.markdown("Upload an MRI image or select from test images to run tumor segmentation.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Input Image")
        
        # Upload option
        uploaded = st.file_uploader("Upload MRI Image", type=["png", "jpg", "jpeg"], help="Upload a brain MRI scan")
        
        # Test images selection
        st.markdown("**Or select from test images:**")
        image_list = []
        if TEST_IMAGES_DIR.exists():
            for p in sorted(TEST_IMAGES_DIR.iterdir()):
                if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                    image_list.append(p)
        
        selected_image = None
        if image_list:
            img_choice = st.selectbox("Choose test image:", options=["None"] + [p.name for p in image_list])
            if img_choice != "None":
                selected_image = TEST_IMAGES_DIR / img_choice
        
        # Display selected/uploaded image
        if uploaded is not None:
            st.image(uploaded, caption="Uploaded Image", use_container_width=True)
        elif selected_image:
            st.image(str(selected_image), caption=selected_image.name, use_container_width=True)
        else:
            st.info("👆 Please upload an image or select from test images")
        
        # Prediction button
        run = st.button("🚀 Run Segmentation", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Results")
        
        if run:
            if uploaded is None and selected_image is None:
                st.error("❌ No image selected or uploaded!")
            else:
                file_bytes = None
                filename = None
                if uploaded is not None:
                    file_bytes = uploaded.read()
                    filename = uploaded.name
                else:
                    filename = selected_image.name
                    file_bytes = selected_image.read_bytes()
                
                with st.spinner("🔄 Running segmentation model..."):
                    try:
                        files = {'file': (filename, file_bytes, mimetypes.guess_type(filename)[0] or 'image/png')}
                        resp = requests.post(f"{backend_url}/predict", files=files, timeout=60)
                    except Exception as e:
                        st.error(f"❌ Request failed: {e}")
                        resp = None
                
                if resp is None:
                    st.warning("⚠️ No response from backend. Make sure the backend is running!")
                elif resp.status_code == 200:
                    data = resp.json()
                    st.success("✅ Segmentation Complete!")
                    
                    # Metrics
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("🎯 Tumor Percentage", f"{data.get('tumor_percentage', 0):.2f}%")
                    with col_b:
                        st.metric("📍 Tumor Pixels", f"{data.get('tumor_pixels', 0):,}")
                    
                    st.caption(f"Total pixels analyzed: {data.get('total_pixels', 0):,}")
                    
                    # Segmentation overlay
                    seg_b64 = data.get('segmented_image')
                    if seg_b64:
                        seg_bytes = base64.b64decode(seg_b64)
                        st.markdown("**🖼️ Segmentation Overlay**")
                        st.image(io.BytesIO(seg_bytes), caption="Tumor regions highlighted in red with green contours", use_container_width=True)
                    
                    # Binary mask
                    mask_b64 = data.get('mask')
                    if mask_b64:
                        mask_bytes = base64.b64decode(mask_b64)
                        with st.expander("Show binary mask"):
                            st.image(io.BytesIO(mask_bytes), caption="Binary segmentation mask", use_container_width=True)
                else:
                    try:
                        st.error(f"❌ Backend error {resp.status_code}: {resp.json()}")
                    except Exception:
                        st.error(f"❌ Backend error {resp.status_code}: {resp.text}")
        else:
            st.info("👈 Configure input and click 'Run Segmentation' to begin")

st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Make sure the backend is running at the configured URL")

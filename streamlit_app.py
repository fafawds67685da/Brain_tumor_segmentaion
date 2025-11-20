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
    "cap 1": {
        "heading": "📊 1. Dataset Overview",
        "description": "Tumor distribution and 3D MRI volumes analysis",
        "has_captions": True
    },
    "cap 2": {
        "heading": "📈 2. Tumor & Intensity Statistics", 
        "description": "Tumor percentage distribution and MRI intensity statistics",
        "has_captions": True
    },
    "cap 3": {
        "heading": "📦 3. Dataset Split Summary",
        "description": "Train, validation, and test set sizes",
        "has_captions": False
    },
    "cap 4": {
        "heading": "🔬 4. Slice-Level Analysis",
        "description": "Tumor pixels, intensity distribution, and feature correlations",
        "has_captions": True
    },
    "cap 5": {
        "heading": "🎨 5. Data Augmentation",
        "description": "Augmentation examples and intensity shift analysis",
        "has_captions": True
    },
    "cap 6": {
        "heading": "📉 6. Training Metrics",
        "description": "Loss, accuracy, and dice coefficient curves",
        "has_captions": False
    }
}

def parse_captions(caption_text):
    """Parse caption.txt file to extract individual captions with their numbers/titles"""
    captions = {}
    lines = caption_text.strip().split('\n')
    current_num = None
    current_text = []
    
    for line in lines:
        # Check if line starts with a number (e.g., "1. ", "2. ", etc.)
        if line.strip() and line[0].isdigit() and '. ' in line:
            # Save previous caption if exists
            if current_num is not None:
                captions[current_num] = '\n'.join(current_text).strip()
            # Start new caption
            parts = line.split('. ', 1)
            current_num = int(parts[0].strip())
            current_text = [parts[1] if len(parts) > 1 else '']
        elif line.startswith('⭐'):
            # Alternative format with stars
            if current_num is not None:
                captions[current_num] = '\n'.join(current_text).strip()
            # Extract caption number from following content or use sequential
            current_num = len(captions) + 1
            current_text = [line]
        elif current_num is not None:
            current_text.append(line)
    
    # Save last caption
    if current_num is not None:
        captions[current_num] = '\n'.join(current_text).strip()
    
    return captions

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
        
        # Read and parse captions if exists
        captions = {}
        caption_file = folder_path / "caption.txt"
        if caption_file.exists() and folder_meta.get("has_captions", False):
            caption_text = caption_file.read_text(encoding='utf-8', errors='ignore')
            captions = parse_captions(caption_text)
        elif caption_file.exists():
            # For folders without numbered captions (cap 3, cap 6), show as single block
            caption_text = caption_file.read_text(encoding='utf-8', errors='ignore')
            with st.expander("📝 About this section", expanded=True):
                st.markdown(caption_text)
        
        # Get all HTML and JSON files in the folder
        html_files = sorted(folder_path.glob("*.html"))
        json_files = sorted(folder_path.glob("*.json"))
        
        # Display HTML visualizations with captions
        if html_files:
            st.subheader("📊 Visualizations")
            for idx, html_file in enumerate(html_files, start=1):
                st.markdown(f"### {html_file.stem.replace('_', ' ').title()}")
                
                # Try to load via backend first, fallback to local
                served_url = f"{backend_url}/stats/{html_file.relative_to(STATS_DIR).as_posix()}"
                try:
                    components.iframe(served_url, height=600, scrolling=True)
                except Exception:
                    html_content = html_file.read_text(encoding='utf-8', errors='ignore')
                    components.html(html_content, height=600, scrolling=True)
                
                # Display caption below the graph if available
                if idx in captions:
                    st.info(f"📝 {captions[idx]}")
                
                st.markdown("---")
        
        # Display JSON data
        if json_files:
            st.subheader("📋 Numerical Statistics")
            for idx, json_file in enumerate(json_files, start=len(html_files) + 1):
                st.markdown(f"### {json_file.stem.replace('_', ' ').title()}")
                
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
                    
                    # Special handling for augmentation stats
                    elif "original_mean_intensity" in data and "augmented_means" in data:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Mean Intensity", f"{data['original_mean_intensity']:.6f}")
                        with col2:
                            st.metric("Augmentation Shift Std", f"{data['augmentation_shift_std']:.6f}")
                        
                        st.markdown("**Augmented Mean Intensities:**")
                        aug_means = data['augmented_means']
                        cols = st.columns(min(len(aug_means), 3))
                        for i, mean_val in enumerate(aug_means):
                            with cols[i % 3]:
                                st.metric(f"Sample {i+1}", f"{mean_val:.6f}")
                    
                    # Special handling for dataset intensity and tumor stats (cap 2)
                    elif "average_tumor_percentage" in data and "intensity_stats" in data:
                        st.metric("Average Tumor Percentage", f"{data['average_tumor_percentage']:.4f}%")
                        
                        st.markdown("**📊 Intensity Statistics by Patient**")
                        import pandas as pd
                        # Paging logic for stats 2
                        key2 = f"stats2_page_{json_file.name}"
                        if key2 not in st.session_state:
                            st.session_state[key2] = 0
                        page_size2 = 10
                        start2 = st.session_state[key2] * page_size2
                        end2 = start2 + page_size2
                        # Add correct index column for paging
                        page_rows = data['intensity_stats'][start2:end2]
                        if page_rows:
                            df2 = pd.DataFrame(page_rows)
                            df2.insert(0, "Index", range(start2 + 1, start2 + 1 + len(df2)))
                            st.dataframe(df2, use_container_width=True)
                            st.info(f"💡 Showing rows {start2+1} to {min(end2, len(data['intensity_stats']))} of {len(data['intensity_stats'])}")
                        col_next2, _ = st.columns(2)
                        if col_next2.button("Next", key=f"next_stats2_{json_file.name}"):
                            if end2 < len(data['intensity_stats']):
                                st.session_state[key2] += 1
                        if st.session_state[key2] > 0:
                            if col_next2.button("Previous", key=f"prev_stats2_{json_file.name}"):
                                st.session_state[key2] -= 1
                    
                    # Special handling for slice-level statistics (cap 4)
                    elif "summary_statistics" in data and "sample_rows" in data:
                        st.markdown("**📊 Summary Statistics**")
                        
                        # Display summary stats for each metric
                        stats = data['summary_statistics']
                        for metric_name, metric_data in stats.items():
                            st.markdown(f"**{metric_name}:**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Mean", f"{metric_data['mean']:.4f}")
                            with col2:
                                st.metric("Std Dev", f"{metric_data['std']:.4f}")
                            with col3:
                                st.metric("Min", f"{metric_data['min']:.4f}")
                            with col4:
                                st.metric("Max", f"{metric_data['max']:.4f}")
                        
                        st.markdown("**📋 Sample Data**")
                        import pandas as pd
                        # Paging logic for stats 4
                        key4 = f"stats4_page_{json_file.name}"
                        if key4 not in st.session_state:
                            st.session_state[key4] = 0
                        page_size4 = 5
                        start4 = st.session_state[key4] * page_size4
                        end4 = start4 + page_size4
                        df4 = pd.DataFrame(data['sample_rows'][start4:end4])
                        st.dataframe(df4, use_container_width=True)
                        st.info(f"💡 Showing rows {start4+1} to {min(end4, len(data['sample_rows']))} of {len(data['sample_rows'])}")
                        col_next4, _ = st.columns(2)
                        if col_next4.button("Next", key=f"next_stats4_{json_file.name}"):
                            if end4 < len(data['sample_rows']):
                                st.session_state[key4] += 1
                        if st.session_state[key4] > 0:
                            if col_next4.button("Previous", key=f"prev_stats4_{json_file.name}"):
                                st.session_state[key4] -= 1
                    
                    else:
                        # Generic JSON display
                        st.json(data)
                    
                    # Display caption below JSON if available
                    if idx in captions:
                        st.info(f"📝 {captions[idx]}")
                    
                    # Show raw JSON in expandable section
                    with st.expander("Show raw JSON data"):
                        st.json(data)
                        
                except Exception as e:
                    st.error(f"Error loading JSON: {e}")
                
                st.markdown("---")


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

import streamlit as st
from pathlib import Path
import requests
import base64
import io
import os
import mimetypes
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
STATS_DIR = ROOT / "Stats"
TEST_IMAGES_DIR = ROOT / "Test_images"

st.set_page_config(page_title="Brain Tumor Stats & Demo", layout="wide")

st.title("Brain Tumor Segmentation — Stats Explorer & Demo")

backend_url = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

# Sidebar: Stats browser
st.sidebar.header("Statistics Reports")
if not STATS_DIR.exists():
    st.sidebar.warning(f"Stats folder not found at {STATS_DIR}")
    stats_map = {}
else:
    stats_map = {}
    for html_file in STATS_DIR.rglob("*.html"):
        rel = html_file.relative_to(STATS_DIR)
        stats_map[str(rel)] = html_file

selected_report = None
if stats_map:
    selected = st.sidebar.selectbox("Choose report (HTML)", options=sorted(stats_map.keys()))
    selected_report = stats_map[selected]
    st.sidebar.markdown(f"**Path:** `{selected_report}`")

# Sidebar: Test images
st.sidebar.header("Test Images")
image_list = []
if TEST_IMAGES_DIR.exists():
    for p in sorted(TEST_IMAGES_DIR.iterdir()):
        if p.is_file() and p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
            image_list.append(p)

selected_image = None
if image_list:
    img_choice = st.sidebar.selectbox("Choose test image", options=[p.name for p in image_list])
    selected_image = TEST_IMAGES_DIR / img_choice
else:
    st.sidebar.info("No test images found in Test_images/")

col1, col2 = st.columns((2, 1))

with col1:
    st.header("Statistics Report Viewer")
    if selected_report:
        st.subheader(selected_report.name)
        # If backend is running we can iframe the served HTML, otherwise render raw HTML
        served_url = f"{backend_url}/stats/{selected_report.relative_to(STATS_DIR).as_posix()}"
        st.markdown("**Preview via backend (iframe)**")
        try:
            components.iframe(served_url, height=700)
        except Exception:
            st.markdown("Could not load report via backend. Rendering static HTML locally below.")
            html_text = selected_report.read_text(encoding='utf-8', errors='ignore')
            components.html(html_text, height=700, scrolling=True)
    else:
        st.info("Select a report from the sidebar to preview it here.")

with col2:
    st.header("Model Demo")
    st.markdown("Upload or choose a test image and press 'Run prediction' to call the backend `/predict` endpoint.")

    uploaded = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
    if uploaded is not None:
        st.image(uploaded, caption="Uploaded image", use_column_width=True)

    if selected_image and uploaded is None:
        st.image(str(selected_image), caption=selected_image.name, use_column_width=True)

    run = st.button("Run prediction")

    if run:
        # Choose file either uploaded or selected_image
        if uploaded is None and selected_image is None:
            st.error("No image selected or uploaded")
        else:
            file_bytes = None
            filename = None
            if uploaded is not None:
                file_bytes = uploaded.read()
                filename = uploaded.name
            else:
                filename = selected_image.name
                file_bytes = selected_image.read_bytes()

            with st.spinner("Sending image to backend..."):
                try:
                    files = {'file': (filename, file_bytes, mimetypes.guess_type(filename)[0] or 'image/png')}
                    resp = requests.post(f"{backend_url}/predict", files=files, timeout=60)
                except Exception as e:
                    st.error(f"Request failed: {e}")
                    resp = None

            if resp is None:
                st.warning("No response from backend")
            else:
                if resp.status_code == 200:
                    data = resp.json()
                    st.success("Prediction received")
                    st.metric("Tumor percentage", f"{data.get('tumor_percentage', 'N/A')} %")
                    st.write(f"Tumor pixels: {data.get('tumor_pixels')} / {data.get('total_pixels')}")

                    # Display segmented image
                    seg_b64 = data.get('segmented_image')
                    mask_b64 = data.get('mask')
                    if seg_b64:
                        seg_bytes = base64.b64decode(seg_b64)
                        st.image(io.BytesIO(seg_bytes), caption="Segmented overlay", use_column_width=True)
                    if mask_b64:
                        mask_bytes = base64.b64decode(mask_b64)
                        st.image(io.BytesIO(mask_bytes), caption="Mask (binary)", use_column_width=True)

                else:
                    try:
                        st.error(f"Backend error {resp.status_code}: {resp.json()}")
                    except Exception:
                        st.error(f"Backend error {resp.status_code}: {resp.text}")

st.markdown("---")
st.caption("Notes: the Streamlit app tries to load the report via the backend at /stats/<path>. If your backend is not running, the app will attempt to render the HTML locally.")

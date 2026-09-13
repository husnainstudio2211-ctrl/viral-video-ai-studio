import streamlit as st
import requests
import json
import base64

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="🎬", layout="wide")

# Styling
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%); color: #ffffff; }
    section[data-testid="stFileUploadDropzone"] small { display: none !important; }
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 3px dashed #818cf8 !important;
        border-radius: 24px !important;
        padding: 80px 40px !important;
        text-align: center !important;
    }
    .header-title {
        text-align: center; font-size: 40px; font-weight: 900;
        background: linear-gradient(90deg, #a5b4fc, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown("---")

_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    uploaded_file = st.file_uploader("Upload File", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("ANALYZE"):
            with st.spinner("🤖 Processing with Gemini API..."):
                api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
                
                # Direct REST Call
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                video_bytes = uploaded_file.read()
                base64_video = base64.b64encode(video_bytes).decode("utf-8")
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Analyze this video for high CTR titles, hooks, and retention factors."},
                            {
                                "inline_data": {
                                    "mime_type": uploaded_file.type,
                                    "data": base64_video
                                }
                            }
                        ]
                    }]
                }
                
                headers = {'Content-Type': 'json'}
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    res_data = response.json()
                    try:
                        text = res_data['candidates'][0]['content']['parts'][0]['text']
                        st.success("✅ Analysis Complete!")
                        st.markdown(text)
                    except Exception:
                        st.json(res_data)
                else:
                    st.error(f"Google API Error ({response.status_code}): {response.text}")

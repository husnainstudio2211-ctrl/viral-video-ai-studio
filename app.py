import streamlit as st
import google.generativeai as genai
import tempfile
import os

# Page Config
st.set_page_config(
    page_title="AI VIRAL STUDIO",
    page_icon="🎬",
    layout="wide"
)

# Ultra-Modern Clean Custom CSS
st.markdown("""
<style>
    /* Dark Premium Gradient Background */
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%);
        color: #ffffff;
    }

    /* Hide Default Streamlit Boring Subtext (200MB, file types, etc.) */
    section[data-testid="stFileUploadDropzone"] small {
        display: none !important;
    }
    
    /* Huge Glowing Centered Upload Zone */
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 3px dashed #818cf8 !important;
        border-radius: 24px !important;
        padding: 90px 40px !important;
        text-align: center !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease-in-out;
    }

    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #c084fc !important;
        box-shadow: 0 0 30px rgba(192, 132, 252, 0.6);
        background: rgba(30, 41, 59, 0.8) !important;
    }

    /* Vibrant Gradient Heading for Upload */
    .upload-label {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 1.5px;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* Huge Glowing ANALYZE Button */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        padding: 20px 40px !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.5);
        transition: all 0.3s ease-in-out;
        margin-top: 20px !important;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 40px rgba(168, 85, 247, 0.8);
    }

    .header-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #a5b4fc, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header-sub {
        text-align: center;
        color: #94a3b8;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
_, header_col, _ = st.columns([1, 2, 1])
with header_col:
    sub_col1, sub_col2 = st.columns([1, 3])
    with sub_col1:
        st.image("logo ah.jpg", width=110)
    with sub_col2:
        st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-sub">PRO VIDEO ANALYTICS ENGINE</div>', unsafe_allow_html=True)

st.markdown("---")

# Centered Bada Upload Section
_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    st.markdown('<div class="upload-label">⚡ UPLOAD FILE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("ANALYZE"):
            with st.spinner("🤖 AI Video Processing in Progress..."):
                try:
                    # Environment variable / Secrets se key uthana
                    api_key = st.secrets.get("GEMINI_API_KEY")
                    if not api_key:
                        st.error("API Key missing! Streamlit Secrets mein GEMINI_API_KEY add karein.")
                    else:
                        genai.configure(api_key=api_key)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name
                        
                        video_file = genai.upload_file(tmp_path)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = """
                        Perform a professional viral strategy breakdown for this video:
                        1. 🎯 **5 High-CTR Viral Titles**
                        2. 🎣 **First 3-Second Hook Optimization**
                        3. 📈 **Video Strengths & Audience Retention Factors**
                        4. 🏷️ **Trending Hashtags & SEO Keywords**
                        5. 💡 **Actionable Call-To-Action (CTA)**
                        """
                        
                        response = model.generate_content([video_file, prompt])
                        st.success("✅ Analysis Complete!")
                        st.markdown(response.text)
                        
                        os.remove(tmp_path)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

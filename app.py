import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. Page Config
st.set_page_config(
    page_title="AI VIRAL VIDEO STUDIO PRO",
    page_icon="🎬",
    layout="wide"
)

# 2. Futuristic Glassmorphism Dark UI (Custom CSS)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Upload Dropzone Styling - Centered & Large */
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 2px dashed #818cf8 !important;
        border-radius: 20px !important;
        padding: 50px 20px !important;
        text-align: center !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        border-color: #c084fc !important;
        box-shadow: 0 0 30px rgba(192, 132, 252, 0.5);
        transform: translateY(-2px);
    }
    
    /* Main Action Button - Big & Glowing */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        padding: 18px 32px !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(168, 85, 247, 0.7);
    }
    
    .centered-title {
        text-align: center;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 1.5px;
        background: linear-gradient(90deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .centered-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section (Centered Alignment)
_, header_col, _ = st.columns([1, 2, 1])
with header_col:
    sub_col1, sub_col2 = st.columns([1, 3])
    with sub_col1:
        st.image("logo ah.jpg", width=110)
    with sub_col2:
        st.markdown('<div class="centered-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
        st.markdown('<div class="centered-subtitle">🚀 Ultra-Fast AI Video Analytics & Growth Engine</div>', unsafe_allow_html=True)

st.markdown("---")

# 4. Centered File Upload Section
_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    st.markdown("<h3 style='text-align: center; font-weight: 700; color: #e2e8f0;'>⚡ Upload Your Video for AI Analysis</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        st.write("") # Spacing
        if st.button("🔥 ANALYZE & GENERATE VIRAL REPORT"):
            with st.spinner("🤖 AI is reading your video content..."):
                try:
                    api_key = st.secrets.get("GEMINI_API_KEY")
                    if not api_key:
                        st.error("API Key missing! Check Streamlit Secrets.")
                    else:
                        genai.configure(api_key=api_key)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name
                        
                        video_file = genai.upload_file(tmp_path)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = """
                        Perform a deep viral strategy breakdown for this video:
                        1. 🎯 **5 High-CTR Viral Titles**
                        2. 🎣 **First 3-Second Hook Optimization**
                        3. 📈 **Video Strengths & Retention Killers**
                        4. 🏷️ **Trending Hashtags & SEO Keywords**
                        5. 💡 **Actionable Call-To-Action (CTA)**
                        """
                        
                        response = model.generate_content([video_file, prompt])
                        st.success("✅ Analysis Complete!")
                        st.markdown(response.text)
                        
                        os.remove(tmp_path)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

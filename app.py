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

# Custom Styling
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle at top, #1e1b4b 0%, #0f172a 100%); color: #ffffff; }
    section[data-testid="stFileUploadDropzone"] small { display: none !important; }
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 3px dashed #818cf8 !important;
        border-radius: 24px !important;
        padding: 90px 40px !important;
        text-align: center !important;
    }
    .upload-label {
        text-align: center; font-size: 28px; font-weight: 800;
        background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important; font-size: 24px !important; font-weight: 900 !important;
        padding: 20px 40px !important; border-radius: 16px !important; border: none !important;
    }
    .header-title {
        text-align: center; font-size: 42px; font-weight: 900;
        background: linear-gradient(90deg, #a5b4fc, #c084fc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown("---")

# Main Interface
_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    st.markdown('<div class="upload-label">⚡ UPLOAD FILE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("ANALYZE"):
            with st.spinner("🤖 AI Video Processing in Progress..."):
                try:
                    # Streamlit Secrets se key extract karna
                    raw_key = st.secrets.get("GEMINI_API_KEY", "").strip()
                    
                    if not raw_key:
                        st.error("Secrets mein GEMINI_API_KEY nahi mili!")
                    else:
                        # Client Configuration
                        genai.configure(api_key=raw_key, client_options={"api_endpoint": "generativelanguage.googleapis.com"})
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            tmp_file.write(uploaded_file.read())
                            tmp_path = tmp_file.name
                        
                        video_file = genai.upload_file(tmp_path)
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        prompt = """
                        Perform a professional viral strategy breakdown:
                        1. 🎯 5 High-CTR Viral Titles
                        2. 🎣 First 3-Second Hook Optimization
                        3. 📈 Audience Retention Factors
                        4. 🏷️ Trending Hashtags & SEO Keywords
                        5. 💡 Actionable Call-To-Action (CTA)
                        """
                        
                        response = model.generate_content([video_file, prompt])
                        st.success("✅ Analysis Complete!")
                        st.markdown(response.text)
                        
                        os.remove(tmp_path)
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

import streamlit as st
import google.generativeai as genai
import tempfile
import os

# 1. Page Config
st.set_page_config(
    page_title="AI Viral Video Studio Pro",
    page_icon="🎬",
    layout="wide"
)

# 2. Dark Premium CSS Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
    }
    section[data-testid="stFileUploadDropzone"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 2px dashed #6366f1 !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Custom Logo & Header Display
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo ah.jpg", width=130)
with col2:
    st.title("AI VIRAL VIDEO STUDIO")
    st.caption("🚀 Professional AI-Powered Video Analytics & Growth Engine")

st.markdown("---")

# 4. Upload & Video Analysis Section
uploaded_file = st.file_uploader("Apni video upload karein (.mp4, .mov)", type=["mp4", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("✨ Analyze & Generate Viral Strategy"):
        with st.spinner("AI is analyzing your video for viral potential..."):
            try:
                api_key = st.secrets.get("GEMINI_API_KEY")
                if not api_key:
                    st.error("API Key nahi mili! Streamlit Secrets check karein.")
                else:
                    genai.configure(api_key=api_key)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    video_file = genai.upload_file(tmp_path)
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = """
                    Is video ko detail se analyze karein aur professional viral strategy report banayein:
                    1. **Viral Title Suggestions** (5 catchy & high CTR titles)
                    2. **Engaging Hook Ideas** (Pehle 3 seconds mein audience ko rokne ke liye)
                    3. **Viral Content Breakdown** (Video ke strong & weak points)
                    4. **SEO Hashtags & Keywords** (TikTok, YouTube Shorts, Reels ke liye)
                    5. **Call to Action (CTA)** (Engagement badhane ke liye)
                    """
                    
                    response = model.generate_content([video_file, prompt])
                    
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    
                    os.remove(tmp_path)
            except Exception as e:
                st.error(f"Error: {str(e)}")

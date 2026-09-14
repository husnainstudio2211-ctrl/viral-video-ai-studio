import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="👑", layout="wide")

# Custom UI Styling - LUXURY THEME
st.markdown("""
<style>
    /* Main Background - Deep Luxury Dark */
    .stApp { 
        background: linear-gradient(135deg, #050505 0%, #1a1a1a 100%); 
        color: #ffffff; 
    }
    
    /* Hide unnecessary text in uploader */
    section[data-testid="stFileUploadDropzone"] small { display: none !important; }
    
    /* HUGE Uploader Box - Glassmorphism & Gold */
    section[data-testid="stFileUploadDropzone"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed #d4af37 !important; /* Luxury Gold */
        border-radius: 30px !important;
        padding: 180px 40px !important; /* MASSIVE PADDING FOR HUGE BUTTON */
        text-align: center !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
    }
    section[data-testid="stFileUploadDropzone"]:hover {
        border: 2px solid #f9f295 !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* Premium Title */
    .header-title {
        text-align: center; 
        font-size: 55px; 
        font-weight: 900;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .header-subtitle {
        text-align: center;
        font-size: 18px;
        color: #a0a0a0;
        margin-bottom: 40px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Luxury Analyze Button */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #bf953f 0%, #fcf6ba 50%, #b38728 100%) !important;
        color: #000000 !important; 
        font-size: 26px !important; 
        font-weight: 900 !important;
        padding: 22px 30px !important; 
        border-radius: 18px !important; 
        border: none !important;
        box-shadow: 0px 8px 25px rgba(191, 149, 63, 0.3);
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 10px 30px rgba(191, 149, 63, 0.5);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Premium Video Strategy Analyzer</div>', unsafe_allow_html=True)
st.markdown("---")

# Making the center column wider for a massive upload box
_, main_col, _ = st.columns([1, 4, 1]) 

with main_col:
    uploaded_file = st.file_uploader("Drop your premium video here", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ ANALYZE VIDEO ✨"):
            with st.spinner("🤖 AI Processing Luxury Strategy..."):
                try:
                    token = st.secrets.get("GEMINI_API_KEY", "").strip()
                    
                    if not token:
                        st.error("Streamlit Secrets mein GEMINI_API_KEY missing hai!")
                    else:
                        video_bytes = uploaded_file.read()
                        base64_video = base64.b64encode(video_bytes).decode("utf-8")
                        
                        # Fixing 404 Error: Changed model name to gemini-1.5-flash-latest
                        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
                        headers = {
                            "x-goog-api-key": token,
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"text": "Perform a professional, high-end viral strategy breakdown for this video: 1. 5 High-CTR Viral Titles, 2. First 3-Second Hook Optimization, 3. Audience Retention Factors, 4. Trending Hashtags & SEO Keywords, 5. Actionable Call-To-Action (CTA). Format the response professionally."},
                                    {
                                        "inline_data": {
                                            "mime_type": uploaded_file.type,
                                            "data": base64_video
                                        }
                                    }
                                ]
                            }]
                        }
                        
                        response = requests.post(url, headers=headers, json=payload)
                        
                        if response.status_code == 200:
                            res_json = response.json()
                            text = res_json['candidates'][0]['content']['parts'][0]['text']
                            st.success("✅ Premium Analysis Complete!")
                            st.markdown(text)
                        else:
                            st.error(f"Google API Error ({response.status_code}): {response.text}")
                            
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

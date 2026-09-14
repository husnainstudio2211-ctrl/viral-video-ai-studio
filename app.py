import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="👑", layout="wide")

# Custom UI Styling - ULTRA LUXURY THEME
st.markdown("""
<style>
    /* Main Background - Deep Luxury Dark */
    .stApp { 
        background: linear-gradient(135deg, #050505 0%, #121212 100%); 
        color: #ffffff; 
    }
    
    /* Completely Hide the "200MB per file" and other default text */
    [data-testid="stFileUploadDropzone"] div div::before { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    [data-testid="stFileUploadDropzone"] > div > span { display: none !important; }
    .st-emotion-cache-1wmy9hl { display: none !important; }
    .st-emotion-cache-8s84i0 { display: none !important; }
    
    /* Hiding the default instructions */
    [data-testid="stFileUploadDropzone"] div div {
        color: transparent !important;
    }

    /* HUGE Uploader Box - Glassmorphism & Gold */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(212, 175, 55, 0.03) !important;
        border: 2px dashed #d4af37 !important; /* Luxury Gold */
        border-radius: 30px !important;
        padding: 120px 20px !important; /* MASSIVE HEIGHT */
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border: 2px solid #fcf6ba !important;
        background: rgba(212, 175, 55, 0.08) !important;
    }

    /* Making the Browse/Upload Button HUGE and Premium */
    [data-testid="stFileUploadDropzone"] button {
        background: linear-gradient(90deg, #bf953f 0%, #fcf6ba 50%, #b38728 100%) !important;
        color: #000000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        padding: 20px 50px !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0px 8px 25px rgba(191, 149, 63, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transform: scale(1.3) !important; /* Enlarges the button significantly */
        visibility: visible !important;
    }
    [data-testid="stFileUploadDropzone"] button:hover {
        transform: scale(1.35) !important;
        box-shadow: 0px 10px 30px rgba(191, 149, 63, 0.6) !important;
    }

    /* Premium Title */
    .header-title {
        text-align: center; 
        font-size: 60px; 
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
        font-size: 16px;
        color: #a0a0a0;
        margin-bottom: 50px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    /* Luxury Analyze Button */
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #bf953f 0%, #fcf6ba 50%, #b38728 100%) !important;
        color: #000000 !important; 
        font-size: 28px !important; 
        font-weight: 900 !important;
        padding: 25px 30px !important; 
        border-radius: 20px !important; 
        border: none !important;
        box-shadow: 0px 10px 30px rgba(191, 149, 63, 0.3);
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: transform 0.2s;
        margin-top: 20px !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 12px 35px rgba(191, 149, 63, 0.5);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Premium Video Strategy Analyzer</div>', unsafe_allow_html=True)
st.markdown("---")

# Wider column for massive upload box
_, main_col, _ = st.columns([1, 4, 1]) 

with main_col:
    uploaded_file = st.file_uploader(" ", type=["mp4", "mov", "avi", "mkv"]) # Empty string removes label

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("✨ ANALYZE VIDEO ✨"):
            with st.spinner("🤖 AI Processing Luxury Strategy..."):
                try:
                    token = st.secrets.get("GEMINI_API_KEY", "").strip()
                    
                    if not token:
                        st.error("Streamlit Secrets में GEMINI_API_KEY मौजूद नहीं है!")
                    else:
                        video_bytes = uploaded_file.read()
                        base64_video = base64.b64encode(video_bytes).decode("utf-8")
                        
                        # SMART FALLBACK SYSTEM
                        models_to_try = [
                            "gemini-1.5-pro", "gemini-1.5-flash",
                            "gemini-1.5-pro-001", "gemini-1.5-flash-001",
                            "gemini-1.5-pro-002", "gemini-1.5-flash-002"
                        ]
                        
                        success = False
                        
                        for model_name in models_to_try:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
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
                                st.success(f"✅ Premium Analysis Complete! (Powered by {model_name})")
                                st.markdown(text)
                                success = True
                                break
                            elif response.status_code == 404:
                                continue
                            else:
                                st.error(f"API Error ({response.status_code}): {response.text}")
                                success = True
                                break
                                
                        if not success:
                            st.error("Google API Error: आपके अकाउंट पर फिलहाल कोई भी मॉडल काम नहीं कर रहा।")
                            
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

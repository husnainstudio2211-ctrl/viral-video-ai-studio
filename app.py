import streamlit as st
import requests
import base64
import time

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="👑", layout="wide")

# Custom UI Styling - ULTRA LUXURY THEME
st.markdown("""
<style>
    /* Main Background - Deep Luxury Dark */
    .stApp { 
        background: linear-gradient(135deg, #050505 0%, #121212 100%); 
        color: #ffffff; 
    }
    
    /* Completely Hide default text */
    [data-testid="stFileUploadDropzone"] div div::before { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    [data-testid="stFileUploadDropzone"] > div > span { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div { color: transparent !important; }

    /* HUGE Uploader Box - Glassmorphism & Gold */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(212, 175, 55, 0.03) !important;
        border: 2px dashed #d4af37 !important;
        border-radius: 30px !important;
        padding: 120px 20px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        backdrop-filter: blur(10px);
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
        transform: scale(1.3) !important;
        visibility: visible !important;
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
        margin-top: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Premium Video Strategy Analyzer</div>', unsafe_allow_html=True)
st.markdown("---")

_, main_col, _ = st.columns([1, 4, 1]) 

with main_col:
    uploaded_file = st.file_uploader(" ", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("✨ ANALYZE VIDEO ✨"):
            token = st.secrets.get("GEMINI_API_KEY", "").strip()
            
            if not token:
                st.error("Streamlit Secrets में GEMINI_API_KEY मौजूद नहीं है!")
            else:
                try:
                    # SMART HEADER DETECTION (For both Standard & AQ. OAuth tokens)
                    if token.startswith("AQ") or token.startswith("ya29"):
                        auth_headers = {"Authorization": f"Bearer {token}"}
                    else:
                        auth_headers = {"x-goog-api-key": token}

                    video_bytes = uploaded_file.read()
                    
                    # STEP 1: UPLOAD VIDEO USING FILE API (Required for Videos)
                    with st.spinner("📤 Uploading video to AI Server..."):
                        upload_url = "https://generativelanguage.googleapis.com/upload/v1beta/files"
                        upload_headers = {
                            **auth_headers,
                            "X-Goog-Upload-Protocol": "raw",
                            "X-Goog-Upload-Command": "start, upload, finalize",
                            "X-Goog-Upload-Header-Content-Length": str(len(video_bytes)),
                            "X-Goog-Upload-Header-Content-Type": uploaded_file.type,
                            "Content-Type": uploaded_file.type
                        }
                        
                        upload_res = requests.post(upload_url, headers=upload_headers, data=video_bytes)
                        
                        if upload_res.status_code != 200:
                            st.error(f"Upload Failed ({upload_res.status_code}): {upload_res.text}")
                            st.stop()
                            
                        upload_data = upload_res.json()
                        file_uri = upload_data.get("file", {}).get("uri")
                        file_name = upload_data.get("file", {}).get("name")

                    # STEP 2: WAIT FOR VIDEO PROCESSING
                    with st.spinner("⏳ Analyzing video frames (Please wait)..."):
                        status_url = f"https://generativelanguage.googleapis.com/v1beta/{file_name}"
                        for _ in range(30): # Will check for up to 90 seconds
                            status_res = requests.get(status_url, headers=auth_headers)
                            if status_res.status_code == 200:
                                state = status_res.json().get("state")
                                if state == "ACTIVE":
                                    break
                                elif state == "FAILED":
                                    st.error("AI Server failed to process this video format.")
                                    st.stop()
                            time.sleep(3)

                    # STEP 3: GENERATE STRATEGY (AUTO-HUNT)
                    with st.spinner("🤖 Generating Luxury Strategy..."):
                        models_to_try = [
                            "gemini-1.5-pro", "gemini-1.5-flash",
                            "gemini-1.5-pro-001", "gemini-1.5-flash-001"
                        ]
                        
                        success = False
                        
                        for model_name in models_to_try:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
                            headers = {
                                **auth_headers,
                                "Content-Type": "application/json"
                            }
                            
                            payload = {
                                "contents": [{
                                    "parts": [
                                        {"text": "Perform a professional, high-end viral strategy breakdown for this video: 1. 5 High-CTR Viral Titles, 2. First 3-Second Hook Optimization, 3. Audience Retention Factors, 4. Trending Hashtags & SEO Keywords, 5. Actionable Call-To-Action (CTA)."},
                                        {
                                            "fileData": {
                                                "mimeType": uploaded_file.type,
                                                "fileUri": file_uri
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
                            else:
                                # Ab hum yahan error chupayenge nahi, balki agle model par jump karenge
                                continue
                                
                        if not success:
                            st.error("Google API Error: आपके अकाउंट पर फिलहाल कोई भी मॉडल काम नहीं कर रहा या Token Expire हो गया है।")
                            
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

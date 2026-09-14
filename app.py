import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="👑", layout="wide")

# Custom UI Styling - ULTRA LUXURY THEME
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #050505 0%, #121212 100%); color: #ffffff; }
    [data-testid="stFileUploadDropzone"] div div::before { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div small { display: none !important; }
    [data-testid="stFileUploadDropzone"] > div > span { display: none !important; }
    [data-testid="stFileUploadDropzone"] div div { color: transparent !important; }
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
    .header-title {
        text-align: center; font-size: 60px; font-weight: 900;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 4px; margin-bottom: 5px; text-transform: uppercase;
    }
    .header-subtitle {
        text-align: center; font-size: 16px; color: #a0a0a0; margin-bottom: 50px;
        letter-spacing: 3px; text-transform: uppercase;
    }
    div.stButton > button {
        width: 100% !important; background: linear-gradient(90deg, #bf953f 0%, #fcf6ba 50%, #b38728 100%) !important;
        color: #000000 !important; font-size: 28px !important; font-weight: 900 !important;
        padding: 25px 30px !important; border-radius: 20px !important; border: none !important;
        box-shadow: 0px 10px 30px rgba(191, 149, 63, 0.3); text-transform: uppercase;
        letter-spacing: 2px; margin-top: 20px !important;
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
            # Yahan maine tumhari API key direct laga di hai!
            token = "AQ.Ab8RN6LurqxJy1KCsAwI6wfdECGiRbzPyiwDLE2hfgpXkfwckQ"
            
            with st.spinner("🤖 Generating Luxury Strategy..."):
                try:
                    # Video ko Base64 mein convert karna
                    video_bytes = uploaded_file.read()
                    base64_video = base64.b64encode(video_bytes).decode("utf-8")
                    
                    auth_headers = {"x-goog-api-key": token}
                    models_to_try = [
                        "gemini-1.5-pro", "gemini-1.5-flash",
                        "gemini-1.5-pro-001", "gemini-1.5-flash-001"
                    ]
                    
                    success = False
                    last_error = ""
                    
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
                                        "inlineData": {  
                                            "mimeType": uploaded_file.type,  
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
                        else:
                            last_error = f"Model {model_name} Error ({response.status_code}): {response.text}"
                            continue
                            
                    if not success:
                        st.error("❌ Google API Error:")
                        st.code(last_error)
                        
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

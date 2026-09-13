import streamlit as st
import requests
import json
import base64

st.set_page_config(page_title="AI VIRAL STUDIO", page_icon="🎬", layout="wide")

# Custom UI Styling
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
    div.stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important; font-size: 22px !important; font-weight: 800 !important;
        padding: 16px 30px !important; border-radius: 14px !important; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-title">AI VIRAL STUDIO</div>', unsafe_allow_html=True)
st.markdown("---")

_, main_col, _ = st.columns([1, 3, 1])

with main_col:
    uploaded_file = st.file_uploader("Upload File", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("ANALYZE"):
            with st.spinner("🤖 AI Video Processing in Progress..."):
                try:
                    token = st.secrets.get("GEMINI_API_KEY", "").strip()
                    
                    if not token:
                        st.error("Streamlit Secrets mein GEMINI_API_KEY missing hai!")
                    else:
                        video_bytes = uploaded_file.read()
                        base64_video = base64.b64encode(video_bytes).decode("utf-8")
                        
                        # Determine if it's an OAuth Token (AQ.) or Standard API Key (AIzaSy)
                        if token.startswith("AQ."):
                            # Use Bearer Token Authorization for OAuth tokens
                            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                            headers = {
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            }
                        else:
                            # Use standard API key parameter
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={token}"
                            headers = {
                                "Content-Type": "application/json"
                            }
                        
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"text": "Perform a professional viral strategy breakdown for this video: 1. 5 High-CTR Viral Titles, 2. First 3-Second Hook Optimization, 3. Audience Retention Factors, 4. Trending Hashtags & SEO Keywords, 5. Actionable Call-To-Action (CTA)."},
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
                            st.success("✅ Analysis Complete!")
                            st.markdown(text)
                        else:
                            st.error(f"Google API Error ({response.status_code}): {response.text}")
                            
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

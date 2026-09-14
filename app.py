```python
import os
import time
import tempfile
from pathlib import Path

import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Viral Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# LUXURY CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Overall app */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(124, 58, 237, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(14, 165, 233, 0.14),
                transparent 28%
            );
    }

    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Main container */
    .block-container {
        max-width: 1180px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* Header */
    .hero {
        text-align: center;
        padding: 18px 10px 8px 10px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.06);
        font-size: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
        opacity: 0.8;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.68;
        max-width: 760px;
        margin: 0 auto;
    }

    /* Brand */
    .brand {
        text-align: center;
        margin-top: 14px;
        margin-bottom: 35px;
        font-size: 15px;
        opacity: 0.6;
    }

    .brand strong {
        font-size: 18px;
        opacity: 1;
    }

    /* Upload card */
    .upload-card {
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.12);
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.08),
                rgba(255,255,255,0.025)
            );
        box-shadow:
            0 20px 70px rgba(0,0,0,0.18);
        margin-bottom: 22px;
    }

    .upload-title {
        font-size: 25px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 7px;
    }

    .upload-subtitle {
        text-align: center;
        font-size: 14px;
        opacity: 0.62;
        margin-bottom: 18px;
    }

    /* Analyze button */
    .stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 15px;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: 0.3px;
    }

    /* Result cards */
    .result-card {
        padding: 22px;
        margin: 16px 0;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.045);
    }

    .result-heading {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    /* Status */
    .status-text {
        text-align: center;
        font-size: 13px;
        opacity: 0.65;
        margin-top: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 45px;
        padding-top: 22px;
        border-top: 1px solid rgba(255,255,255,0.08);
        opacity: 0.55;
    }

    .footer-name {
        font-size: 22px;
        font-weight: 900;
        opacity: 1;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            AI POWERED • YOUTUBE SEO STUDIO
        </div>

        <div class="hero-title">
            🎬 AI Viral Video Studio
        </div>

        <div class="hero-subtitle">
            Upload your video and let AI understand the video,
            voice and content to create a complete YouTube SEO package.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand">
        Created by <strong>Husnain Akram</strong>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GET API KEY FROM STREAMLIT SECRETS
# ============================================================

def get_api_key():
    """
    API key user ko show nahi hoti.
    Streamlit Cloud Secrets se read hoti hai.
    """

    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")

        if secret_key:
            return str(secret_key).strip()

    except Exception:
        pass

    # Local development fallback
    env_key = os.getenv("GEMINI_API_KEY", "")

    return env_key.strip()


API_KEY = get_api_key()


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = ""

if "video_name" not in st.session_state:
    st.session_state.video_name = ""


# ============================================================
# DAILY LIMIT
# ============================================================

# NOTE:
# Streamlit session-based limit.
# For a true shared 3-per-day limit across all users,
# use a persistent database later.

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

MAX_ANALYSES_PER_SESSION = 3


# ============================================================
# VIDEO UPLOAD AREA
# ============================================================

st.markdown(
    """
    <div class="upload-card">

        <div class="upload-title">
            🎥 Upload Your Video
        </div>

        <div class="upload-subtitle">
            MP4, MOV, AVI, MKV, WEBM and other supported video formats
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


uploaded_video = st.file_uploader(
    "Select your video",
    type=[
        "mp4",
        "mov",
        "avi",
        "mkv",
        "webm",
        "mpeg",
        "mpg",
    ],
    label_visibility="collapsed",
)


# ============================================================
# VIDEO PREVIEW
# ============================================================

if uploaded_video:

    st.session_state.video_name = uploaded_video.name

    st.success(
        f"✅ Video ready: {uploaded_video.name}"
    )

    st.video(uploaded_video)

    size_mb = uploaded_video.size / (1024 * 1024)

    st.markdown(
        f"""
        <div class="status-text">
            Video size: {size_mb:.2f} MB
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYZE PROMPT
# ============================================================

ANALYSIS_PROMPT = """
You are an elite YouTube SEO strategist, video analyst,
content strategist and YouTube growth consultant.

Analyze the uploaded video deeply.

You should understand:
- visual content
- spoken voice
- dialogue
- narration
- important scenes
- main topic
- overall message
- audience
- educational/entertainment value
- tone
- intent
- important keywords

Then create a complete professional YouTube publishing package.

Do not invent facts that are not present in the video.
Do not use deceptive clickbait.
Make titles attractive but truthful.

Return the response using EXACTLY these sections:

# 🔥 1. FIVE BEST YOUTUBE TITLES

Create 5 different, catchy and high-CTR title options.

# 🏆 2. RECOMMENDED BEST TITLE

Choose the strongest title from the 5 options
and briefly explain why.

# 📝 3. SEO-OPTIMIZED DESCRIPTION

Write one professional YouTube description based on the
actual video content.

Include:
- strong opening hook
- natural keywords
- accurate summary
- viewer benefit
- call to action

# 🏷️ 4. YOUTUBE TAGS

Create 25 relevant YouTube search tags.

Return them as one comma-separated line.

# #️⃣ 5. HASHTAGS

Create 10 highly relevant hashtags.

Return them as one line.

# ⏰ 6. BEST UPLOAD TIMING

Give practical YouTube upload timing guidance for Pakistan
Standard Time (PKT).

Include:
- best days
- suggested time windows
- simple testing strategy

Do not guarantee virality.

# 📊 7. VIDEO ANALYSIS

Tell the creator:

- What type of video this is
- Main topic
- Main audience
- Main message
- Tone/style
- Strongest content point
- Weakest content point
- One improvement suggestion

# 🚀 8. SEO GROWTH STRATEGY

Give 5 practical recommendations for:

1. CTR
2. Search discovery
3. Retention
4. Engagement
5. Early performance

Keep everything professional and easy to copy into YouTube Studio.
"""


# ============================================================
# UPLOAD TO GEMINI
# ============================================================

def upload_video(client, streamlit_file):

    extension = Path(
        streamlit_file.name
    ).suffix

    if not extension:
        extension = ".mp4"

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension,
    )

    temp_path = temp_file.name

    try:

        temp_file.write(
            streamlit_file.getvalue()
        )

        temp_file.close()

        gemini_file = client.files.upload(
            file=temp_path
        )

        return gemini_file, temp_path

    except Exception:

        try:
            temp_file.close()
        except Exception:
            pass

        raise


# ============================================================
# WAIT FOR VIDEO PROCESSING
# ============================================================

def wait_for_video(client, gemini_file):

    progress = st.empty()

    while True:

        current_file = client.files.get(
            name=gemini_file.name
        )

        state = getattr(
            current_file,
            "state",
            None
        )

        state_name = getattr(
            state,
            "name",
            str(state)
        )

        if state_name == "ACTIVE":

            progress.success(
                "✅ Video analysis input is ready."
            )

            return current_file

        if state_name in [
            "FAILED",
            "ERROR",
        ]:

            raise RuntimeError(
                f"Gemini video processing failed: {state_name}"
            )

        progress.info(
            f"🎥 Preparing video for AI analysis... {state_name}"
        )

        time.sleep(4)


# ============================================================
# ANALYZE VIDEO WITH GEMINI
# ============================================================

def analyze_video(api_key, video_file):

    client = genai.Client(
        api_key=api_key
    )

    temporary_path = None

    try:

        # Upload video
        with st.spinner(
            "📤 Uploading video to AI..."
        ):

            gemini_file, temporary_path = upload_video(
                client,
                video_file
            )

        # Wait
        gemini_file = wait_for_video(
            client,
            gemini_file
        )

        # Generate result
        with st.spinner(
            "🧠 AI video, voice aur content analyze kar raha hai..."
        ):

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    gemini_file,
                    ANALYSIS_PROMPT,
                ],
            )

        if not response:
            raise RuntimeError(
                "Gemini ne response return nahi kiya."
            )

        if not response.text:
            raise RuntimeError(
                "Gemini ne empty response diya."
            )

        return response.text

    finally:

        if temporary_path:

            try:
                os.remove(
                    temporary_path
                )
            except Exception:
                pass


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze = st.button(
    "✨ ANALYZE VIDEO & GENERATE COMPLETE SEO",
    type="primary",
    use_container_width=True,
)


# ============================================================
# BUTTON ACTION
# ============================================================

if analyze:

    # API secret missing
    if not API_KEY:

        st.error(
            "❌ AI service configuration missing hai."
        )

        st.info(
            "Administrator ko Streamlit Secrets mein "
            "GEMINI_API_KEY set karni hogi."
        )

    # No video
    elif uploaded_video is None:

        st.warning(
            "🎥 Pehle video upload karein."
        )

    # Daily/session limit
    elif st.session_state.analysis_count >= MAX_ANALYSES_PER_SESSION:

        st.error(
            "⛔ Is session ki 3-video analysis limit complete ho gayi hai."
        )

        st.info(
            "Naye session mein limit dobara available ho sakti hai."
        )

    else:

        try:

            result = analyze_video(
                API_KEY,
                uploaded_video
            )

            st.session_state.result = result

            st.session_state.analysis_count += 1

            st.success(
                "🎉 Your complete YouTube SEO package is ready!"
            )

        except Exception as error:

            error_text = str(error)

            st.error(
                "❌ Video analysis complete nahi ho saki."
            )

            if (
                "401" in error_text
                or "403" in error_text
            ):

                st.warning(
                    "AI service authorization issue hai. "
                    "Administrator ki API configuration check karein."
                )

            elif "429" in error_text:

                st.warning(
                    "AI service ki rate/quota limit temporarily hit ho gayi hai."
                )

            elif "404" in error_text:

                st.warning(
                    "Selected AI model/API endpoint available nahi hai."
                )

            elif (
                "size" in error_text.lower()
                or "too large" in error_text.lower()
            ):

                st.warning(
                    "Video file bohat bari hai. "
                    "Choti/compressed video try karein."
                )

            else:

                st.warning(
                    "Unexpected AI error aaya hai."
                )

            st.code(
                error_text
            )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result:

    st.markdown("---")

    st.markdown(
        """
        <div class="result-card">

            <div class="result-heading">
                🏆 Your Premium YouTube SEO Package
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.result
    )

    st.markdown("---")

    st.download_button(
        "📥 Download Complete SEO Package",
        data=st.session_state.result,
        file_name="AI_Viral_Video_Studio_SEO.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ============================================================
# USAGE INDICATOR
# ============================================================

remaining = max(
    0,
    MAX_ANALYSES_PER_SESSION
    - st.session_state.analysis_count
)

st.markdown(
    f"""
    <div class="status-text">
        Analyses used in this session:
        {st.session_state.analysis_count} / {MAX_ANALYSES_PER_SESSION}
        &nbsp; • &nbsp;
        Remaining:
        {remaining}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div class="footer-name">
            Husnain Akram
        </div>

        <div>
            AI Viral Video Studio
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)
```

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
# LUXURY DESIGN
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(124, 58, 237, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(14, 165, 233, 0.12),
                transparent 30%
            );
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 35px;
        padding-bottom: 60px;
    }

    .hero {
        text-align: center;
        padding: 20px 10px 10px 10px;
    }

    .badge {
        display: inline-block;
        padding: 8px 15px;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 12px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 54px;
        font-weight: 900;
        letter-spacing: -2.5px;
        line-height: 1.05;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        max-width: 760px;
        margin: auto;
        font-size: 17px;
        opacity: 0.68;
        line-height: 1.6;
    }

    .creator {
        text-align: center;
        margin-top: 16px;
        margin-bottom: 38px;
        font-size: 14px;
        opacity: 0.60;
    }

    .creator strong {
        font-size: 19px;
        opacity: 1;
    }

    .upload-box {
        padding: 32px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.12);
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.08),
                rgba(255,255,255,0.025)
            );
        box-shadow: 0 24px 80px rgba(0,0,0,0.18);
    }

    .upload-title {
        text-align: center;
        font-size: 28px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .upload-subtitle {
        text-align: center;
        font-size: 14px;
        opacity: 0.62;
        margin-bottom: 22px;
    }

    .result-header {
        font-size: 28px;
        font-weight: 850;
        margin: 30px 0 16px 0;
    }

    .result-card {
        padding: 22px;
        margin: 15px 0;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.04);
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 25px;
        border-top: 1px solid rgba(255,255,255,0.08);
        opacity: 0.55;
    }

    .footer-name {
        font-size: 23px;
        font-weight: 900;
        opacity: 1;
    }

    .stButton > button {
        min-height: 58px;
        border-radius: 15px;
        font-size: 17px;
        font-weight: 850;
        letter-spacing: 0.3px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="badge">
            AI POWERED • YOUTUBE SEO STUDIO
        </div>

        <div class="hero-title">
            🎬 AI Viral Video Studio
        </div>

        <div class="hero-subtitle">
            Upload your video and let AI understand its visuals,
            voice, topic and message to create a complete
            professional YouTube SEO package.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="creator">
        Created by <strong>Husnain Akram</strong>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API KEY FROM STREAMLIT SECRETS
# ============================================================

def get_api_key():
    """
    API key user ko show nahi hoti.
    Streamlit Secrets se read hoti hai.
    """

    try:
        secret = st.secrets.get("GEMINI_API_KEY", "")

        if secret:
            return str(secret).strip()

    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "").strip()


API_KEY = get_api_key()


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = ""

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0


# Maximum analyses per browser session
MAX_ANALYSES = 3


# ============================================================
# VIDEO UPLOAD
# ============================================================

st.markdown(
    """
    <div class="upload-box">

        <div class="upload-title">
            🎥 Upload Your Video
        </div>

        <div class="upload-subtitle">
            AI will analyze the video, voice, topic and overall content.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


uploaded_video = st.file_uploader(
    "Choose your video",
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

if uploaded_video is not None:

    st.success(
        f"✅ Video ready: {uploaded_video.name}"
    )

    st.video(uploaded_video)

    file_size_mb = uploaded_video.size / (1024 * 1024)

    st.caption(
        f"Video size: {file_size_mb:.2f} MB"
    )


# ============================================================
# AI PROMPT
# ============================================================

ANALYSIS_PROMPT = """
You are an elite YouTube SEO strategist,
professional video analyst and YouTube growth consultant.

Analyze the uploaded video carefully.

Understand as much as possible from:
- visual scenes
- spoken voice
- narration
- dialogue
- on-screen text
- topic
- message
- tone
- style
- audience
- educational value
- entertainment value
- important keywords

Then create a complete professional YouTube publishing package.

IMPORTANT RULES:

1. Use the actual uploaded video as the primary source.
2. Do not invent facts that are not present in the video.
3. Do not create deceptive clickbait.
4. Titles should be catchy, interesting and truthful.
5. Description must accurately describe the video.
6. Tags must be directly related to the actual content.
7. Hashtags must be relevant.
8. Do not keyword-stuff.
9. Make the result easy to copy into YouTube Studio.
10. Do not guarantee that a video will go viral.

RETURN EXACTLY THESE SECTIONS:

==================================================
🔥 1. FIVE CATCHY YOUTUBE TITLES
==================================================

Give exactly 5 different title options.

Make them varied:
- curiosity based
- benefit based
- problem/solution
- keyword focused
- emotional/high-CTR

==================================================
🏆 2. BEST TITLE
==================================================

Select the strongest title from the five.

Give a short explanation of why it is the strongest.

==================================================
📝 3. SEO-OPTIMIZED DESCRIPTION
==================================================

Write one professional YouTube description based on
the actual video.

Include:
- strong opening hook
- natural keywords
- accurate video summary
- viewer value
- call to action

==================================================
🏷️ 4. YOUTUBE TAGS
==================================================

Give 25 relevant YouTube tags.

Return them in one comma-separated line.

==================================================
#️⃣ 5. HASHTAGS
==================================================

Give 10 relevant hashtags.

Return them in one line.

==================================================
⏰ 6. BEST UPLOAD TIMING
==================================================

Give practical upload timing recommendations for
Pakistan Standard Time (PKT).

Include:
- best days
- suggested time windows
- simple testing strategy

Do NOT claim any time guarantees virality.

==================================================
📊 7. VIDEO ANALYSIS
==================================================

Explain:

- video type
- main topic
- target audience
- main message
- tone/style
- strongest point
- weakest point
- one important improvement

==================================================
🚀 8. SEO GROWTH STRATEGY
==================================================

Give 5 practical strategies for:

1. CTR
2. Search visibility
3. Audience retention
4. Engagement
5. Early performance

Keep everything professional and useful.
"""


# ============================================================
# UPLOAD VIDEO TO GEMINI
# ============================================================

def upload_video(client, streamlit_file):

    extension = Path(
        streamlit_file.name
    ).suffix

    if not extension:
        extension = ".mp4"

    temporary_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    )

    temporary_path = temporary_file.name

    try:

        temporary_file.write(
            streamlit_file.getvalue()
        )

        temporary_file.close()

        gemini_file = client.files.upload(
            file=temporary_path
        )

        return gemini_file, temporary_path

    except Exception:

        try:
            temporary_file.close()
        except Exception:
            pass

        raise


# ============================================================
# WAIT FOR GEMINI FILE PROCESSING
# ============================================================

def wait_for_video_processing(
    client,
    gemini_file
):

    status_placeholder = st.empty()

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

            status_placeholder.success(
                "✅ Video is ready for AI analysis."
            )

            return current_file

        if state_name in [
            "FAILED",
            "ERROR",
        ]:

            raise RuntimeError(
                f"Gemini video processing failed: {state_name}"
            )

        status_placeholder.info(
            f"🎥 Preparing your video for AI analysis... "
            f"{state_name}"
        )

        time.sleep(5)


# ============================================================
# ANALYZE VIDEO
# ============================================================

def analyze_video(
    api_key,
    streamlit_video
):

    client = genai.Client(
        api_key=api_key
    )

    temporary_path = None

    try:

        with st.spinner(
            "📤 Uploading video to AI..."
        ):

            gemini_file, temporary_path = upload_video(
                client,
                streamlit_video
            )

        gemini_file = wait_for_video_processing(
            client,
            gemini_file
        )

        with st.spinner(
            "🧠 AI is analyzing your video, voice and content..."
        ):

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    gemini_file,
                    ANALYSIS_PROMPT
                ]
            )

        if not response:

            raise RuntimeError(
                "Gemini ne koi response return nahi kiya."
            )

        if not response.text:

            raise RuntimeError(
                "Gemini ne empty response return kiya."
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

st.write("")

analyze_button = st.button(
    "✨ ANALYZE VIDEO & GENERATE COMPLETE SEO",
    type="primary",
    use_container_width=True,
)


# ============================================================
# ANALYZE ACTION
# ============================================================

if analyze_button:

    if not API_KEY:

        st.error(
            "❌ AI service configuration missing hai."
        )

        st.info(
            "Administrator ko Streamlit Secrets mein "
            "GEMINI_API_KEY set karni hogi."
        )

    elif uploaded_video is None:

        st.warning(
            "🎥 Pehle video upload karein."
        )

    elif (
        st.session_state.analysis_count
        >= MAX_ANALYSES
    ):

        st.error(
            "⛔ Is browser session ki 3-video analysis limit complete ho gayi hai."
        )

        st.info(
            "Ye local protection hai. Gemini ki Google-side limits "
            "alag hoti hain."
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
                "🎉 Complete YouTube SEO package ready hai!"
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
                    "Gemini API authorization problem hai. "
                    "Streamlit Secrets mein API key check karein."
                )

            elif "404" in error_text:

                st.warning(
                    "Gemini model/API endpoint available nahi hai."
                )

            elif "429" in error_text:

                st.warning(
                    "Gemini Free Tier ki rate/quota limit hit ho gayi hai."
                )

            elif (
                "size" in error_text.lower()
                or "too large" in error_text.lower()
            ):

                st.warning(
                    "Video file bohat bari hai. "
                    "Smaller/compressed video try karein."
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
        <div class="result-header">
            🏆 Premium YouTube SEO Package
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.result
    )

    st.markdown("---")

    st.download_button(
        label="📥 Download Complete SEO Package",
        data=st.session_state.result,
        file_name="AI_Viral_Video_Studio_SEO.txt",
        mime="text/plain",
        use_container_width=True,
    )


# ============================================================
# USAGE
# ============================================================

remaining = max(
    0,
    MAX_ANALYSES
    - st.session_state.analysis_count
)

st.markdown(
    f"""
    <div class="footer">
        <div class="footer-name">
            Husnain Akram
        </div>

        <div>
            AI Viral Video Studio
        </div>

        <div style="margin-top:10px; font-size:12px;">
            Analyses used in this session:
            {st.session_state.analysis_count}/{MAX_ANALYSES}
            • Remaining: {remaining}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

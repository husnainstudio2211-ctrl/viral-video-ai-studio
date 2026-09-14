
import os
import time
import tempfile
from pathlib import Path

import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Viral Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LUXURY UI
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(120, 80, 255, 0.12),
                transparent 35%
            ),
            radial-gradient(
                circle at top right,
                rgba(0, 180, 255, 0.10),
                transparent 30%
            );
    }

    /* Main title */
    .luxury-title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .luxury-subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 25px;
    }

    /* Brand */
    .brand-box {
        padding: 18px 20px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.03)
        );
        border: 1px solid rgba(255,255,255,0.13);
        margin: 15px 0 25px 0;
    }

    .brand-name {
        font-size: 28px;
        font-weight: 900;
    }

    .brand-text {
        font-size: 13px;
        opacity: 0.65;
    }

    /* Cards */
    .lux-card {
        padding: 22px;
        border-radius: 18px;
        background: rgba(128,128,128,0.07);
        border: 1px solid rgba(128,128,128,0.20);
        margin-bottom: 18px;
    }

    /* Section heading */
    .section-heading {
        font-size: 25px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Small info */
    .small-info {
        font-size: 13px;
        opacity: 0.65;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="luxury-title">🎬 AI Viral Video Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="luxury-subtitle">'
    'Professional AI-powered YouTube SEO & Video Intelligence Studio'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="brand-box">
        <div class="brand-name">Husnain Akram</div>
        <div class="brand-text">
            Created & Designed by Husnain Akram
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API KEY FUNCTION
# ============================================================

def get_secret_api_key():

    # Streamlit Cloud secrets
    try:
        value = st.secrets.get("GEMINI_API_KEY", "")

        if value:
            return str(value).strip()

    except Exception:
        pass

    # Environment variable
    value = os.getenv("GEMINI_API_KEY", "")

    return value.strip()


# ============================================================
# SESSION STATE
# ============================================================

if "api_key" not in st.session_state:

    st.session_state.api_key = get_secret_api_key()


if "generated_result" not in st.session_state:

    st.session_state.generated_result = ""


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🔐 Gemini Setup")

sidebar_key = st.sidebar.text_input(
    "Google AI Studio API Key",
    value=st.session_state.api_key,
    type="password",
    placeholder="AIza..."
)


# Save key in current Streamlit session
if sidebar_key.strip():

    st.session_state.api_key = sidebar_key.strip()

    st.sidebar.success("✅ API key loaded")

else:

    st.sidebar.warning(
        "⚠️ API key required"
    )


st.sidebar.markdown("---")

st.sidebar.markdown("### 🤖 AI Model")

MODEL_NAME = st.sidebar.selectbox(
    "Gemini Model",
    [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-2.5-flash",
    ],
    index=0
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **Usage**

    1. API key ایک بار enter کریں۔
    2. Video upload کریں۔
    3. Analyze button دبائیں۔
    4. نئی video کے لیے دوبارہ video upload کریں۔
    """
)


# ============================================================
# VIDEO UPLOAD
# ============================================================

st.markdown(
    '<div class="section-heading">🎥 Upload Your YouTube Video</div>',
    unsafe_allow_html=True
)

uploaded_video = st.file_uploader(
    "Video select کریں",
    type=[
        "mp4",
        "mov",
        "avi",
        "mkv",
        "webm",
        "mpeg",
        "mpg"
    ],
    help="YouTube video upload کریں تاکہ AI اس کا content analyze کر سکے."
)


# ============================================================
# VIDEO PREVIEW
# ============================================================

if uploaded_video is not None:

    st.success(
        f"✅ Selected: {uploaded_video.name}"
    )

    st.video(uploaded_video)

    size_mb = uploaded_video.size / (1024 * 1024)

    st.caption(
        f"Video Size: {size_mb:.2f} MB"
    )


# ============================================================
# VIDEO DETAILS
# ============================================================

st.markdown(
    '<div class="section-heading">📝 Video Information</div>',
    unsafe_allow_html=True
)

video_topic = st.text_area(
    "Video Topic / Idea (Optional)",
    placeholder=(
        "Example: How to earn money online in Pakistan"
    ),
    height=90
)

target_audience = st.text_input(
    "Target Audience (Optional)",
    placeholder=(
        "Example: Pakistan students, beginners, freelancers"
    )
)

language = st.selectbox(
    "SEO Content Language",
    [
        "Roman Urdu / Hindi",
        "English",
        "Urdu"
    ]
)

category = st.selectbox(
    "Video Category",
    [
        "Education",
        "Technology",
        "How-To / Tutorial",
        "Online Earning",
        "Freelancing",
        "Entertainment",
        "Gaming",
        "News / Updates",
        "Review",
        "Other"
    ]
)


# ============================================================
# PROMPT
# ============================================================

def build_prompt():

    topic = video_topic.strip()

    if not topic:

        topic = (
            "Determine the main topic from the uploaded video."
        )

    audience = target_audience.strip()

    if not audience:

        audience = "General YouTube audience"

    return f"""
You are an elite YouTube SEO strategist,
video content analyst and growth consultant.

Analyze the uploaded video carefully.

Additional information:

Video Topic:
{topic}

Target Audience:
{audience}

Language:
{language}

Category:
{category}

Your objective is to create an accurate,
professional and high-performing YouTube package.

IMPORTANT RULES:

- Analyze the actual uploaded video.
- Do not invent facts.
- Do not create deceptive clickbait.
- Titles should be attractive but truthful.
- Description must accurately match the video.
- Tags must be directly relevant.
- Hashtags must be relevant.
- Avoid keyword stuffing.
- Make the output easy to copy into YouTube Studio.
- Do not guarantee virality.

OUTPUT:

==================================================
🔥 1. FIVE CATCHY TITLES
==================================================

Create exactly 5 title options.

Use different approaches:
- curiosity
- benefit
- problem/solution
- keyword focused
- emotional hook

==================================================
📝 2. SEO-OPTIMIZED DESCRIPTION
==================================================

Write one professional description.

Include:
- powerful opening hook
- natural SEO keywords
- accurate summary
- viewer benefits
- call to action

==================================================
🏷️ 3. YOUTUBE TAGS
==================================================

Create 25 highly relevant tags.

Return them as one comma-separated line.

==================================================
#️⃣ 4. HASHTAGS
==================================================

Create 10 relevant hashtags.

Return them as one line.

==================================================
⏰ 5. BEST UPLOAD TIMING
==================================================

Recommend practical upload times for Pakistan Standard Time (PKT).

Include:
- best days
- suggested time windows
- testing strategy

Do not promise that a time guarantees virality.

==================================================
📈 6. SEO GROWTH STRATEGY
==================================================

Give 5 useful strategies for:
- CTR
- search discovery
- retention
- engagement
- early performance

==================================================
🏆 7. BEST TITLE
==================================================

Select the strongest title from the 5 options.

Explain briefly why you selected it.

==================================================
🎯 8. VIDEO CONTENT SUMMARY
==================================================

Give a short summary of what the uploaded video contains.
"""


# ============================================================
# UPLOAD VIDEO
# ============================================================

def upload_video(client, streamlit_file):

    extension = Path(
        streamlit_file.name
    ).suffix

    if not extension:

        extension = ".mp4"

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    )

    path = temp.name

    try:

        temp.write(
            streamlit_file.getvalue()
        )

        temp.close()

        gemini_file = client.files.upload(
            file=path
        )

        return gemini_file, path

    except Exception:

        try:
            temp.close()
        except Exception:
            pass

        raise


# ============================================================
# WAIT FOR PROCESSING
# ============================================================

def wait_until_active(client, gemini_file):

    status_box = st.empty()

    while True:

        current = client.files.get(
            name=gemini_file.name
        )

        state = getattr(
            current,
            "state",
            None
        )

        if state is None:

            return current

        state_name = getattr(
            state,
            "name",
            str(state)
        )

        if state_name == "ACTIVE":

            status_box.success(
                "✅ Video processing complete."
            )

            return current

        if state_name in (
            "FAILED",
            "ERROR"
        ):

            raise RuntimeError(
                f"Video processing failed: {state_name}"
            )

        status_box.info(
            f"🎥 Gemini processing video... {state_name}"
        )

        time.sleep(5)


# ============================================================
# ANALYZE VIDEO
# ============================================================

def analyze_video(api_key_value):

    client = genai.Client(
        api_key=api_key_value
    )

    temporary_path = None

    try:

        # --------------------------------------------
        # Upload
        # --------------------------------------------

        with st.spinner(
            "📤 Video Gemini ko upload ho rahi hai..."
        ):

            gemini_file, temporary_path = upload_video(
                client,
                uploaded_video
            )

        # --------------------------------------------
        # Processing
        # --------------------------------------------

        gemini_file = wait_until_active(
            client,
            gemini_file
        )

        # --------------------------------------------
        # Prompt
        # --------------------------------------------

        prompt = build_prompt()

        # --------------------------------------------
        # Generate
        # --------------------------------------------

        with st.spinner(
            "🧠 AI video analyze karke professional SEO package bana raha hai..."
        ):

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    gemini_file,
                    prompt
                ]
            )

        if not response:

            raise RuntimeError(
                "Gemini ne response return nahi kiya."
            )

        if not response.text:

            raise RuntimeError(
                "Gemini ne empty text response return kiya."
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

st.markdown("---")

analyze_button = st.button(
    "✨ ANALYZE VIDEO & GENERATE VIRAL SEO",
    type="primary",
    use_container_width=True
)


# ============================================================
# BUTTON ACTION
# ============================================================

if analyze_button:

    # --------------------------------------------
    # Key check
    # --------------------------------------------

    if not st.session_state.api_key:

        st.error(
            "❌ Gemini API key missing hai."
        )

        st.info(
            "Sidebar mein Google AI Studio API key paste karein."
        )

    elif not st.session_state.api_key.startswith(
        "AIza"
    ):

        st.error(
            "❌ API key format incorrect lag raha hai."
        )

        st.info(
            "Google AI Studio wali API key paste karein."
        )

    # --------------------------------------------
    # Video check
    # --------------------------------------------

    elif uploaded_video is None:

        st.warning(
            "⚠️ Pehle video upload karein."
        )

    # --------------------------------------------
    # Generate
    # --------------------------------------------

    else:

        try:

            result = analyze_video(
                st.session_state.api_key
            )

            st.session_state.generated_result = result

            st.success(
                "🎉 Analysis complete!"
            )

        except Exception as error:

            error_text = str(error)

            st.error(
                "❌ AI analysis complete nahi ho saki."
            )

            if (
                "401" in error_text
                or "403" in error_text
            ):

                st.warning(
                    "API key invalid ya unauthorized hai."
                )

            elif "404" in error_text:

                st.warning(
                    "Selected Gemini model/API endpoint issue hai."
                )

            elif "429" in error_text:

                st.warning(
                    "⚠️ Free-tier rate limit hit ho gayi hai."
                )

                st.info(
                    "Nayi API key banana is limit ko unlimited nahi karega, "
                    "kyunki limits project level par apply hoti hain."
                )

            elif (
                "quota" in error_text.lower()
            ):

                st.warning(
                    "Gemini quota/rate limit issue hai."
                )

            elif (
                "size" in error_text.lower()
            ):

                st.warning(
                    "Video file size/input limit ka issue ho sakta hai."
                )

            else:

                st.warning(
                    "Unexpected API error."
                )

            st.code(
                error_text
            )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.generated_result:

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">'
        '🏆 Your Premium YouTube SEO Package'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.generated_result
    )

    st.markdown("---")

    st.download_button(
        "📥 Download Complete SEO Package",
        data=st.session_state.generated_result,
        file_name="AI_Viral_Video_Studio_SEO.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# BRAND FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <div style="font-size:24px; font-weight:900;">
            Husnain Akram
        </div>
        <div style="font-size:12px; opacity:0.55;">
            AI Viral Video Studio
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


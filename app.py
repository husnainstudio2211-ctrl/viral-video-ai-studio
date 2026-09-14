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
    initial_sidebar_state="expanded",
)


# ============================================================
# APP HEADER
# ============================================================

st.title("🎬 AI Viral Video Studio")

st.write(
    "Apni YouTube video upload karein aur AI se "
    "Titles, Description, Tags, Hashtags aur Upload Strategy generate karein."
)

st.markdown("---")


# ============================================================
# API KEY
# ============================================================

def get_saved_api_key():
    """
    API key ko Streamlit Secrets ya environment variable se lene ki koshish.
    """

    # Streamlit Cloud Secrets
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
        if secret_key:
            return secret_key
    except Exception:
        pass

    # Environment variable
    return os.getenv("GEMINI_API_KEY", "")


saved_api_key = get_saved_api_key()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔑 Gemini API")

api_key = st.sidebar.text_input(
    "Google AI Studio API Key",
    value=saved_api_key,
    type="password",
    placeholder="AIza..."
)

if api_key:
    st.sidebar.success("✅ API key available")

else:
    st.sidebar.warning(
        "⚠️ API key enter karein"
    )

st.sidebar.markdown("---")

st.sidebar.info(
    "Google AI Studio se Gemini API key le kar yahan paste karein."
)


# ============================================================
# GEMINI MODEL
# ============================================================

MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# VIDEO UPLOAD
# ============================================================

st.subheader("🎥 Upload Your Video")

uploaded_video = st.file_uploader(
    "Apni YouTube video upload karein:",
    type=[
        "mp4",
        "mov",
        "avi",
        "mkv",
        "webm",
        "mpeg",
        "mpg"
    ],
    help="Video upload karne ke baad Gemini uska content analyze karega."
)


# ============================================================
# VIDEO PREVIEW
# ============================================================

if uploaded_video is not None:

    st.success(
        f"✅ Video selected: {uploaded_video.name}"
    )

    st.video(
        uploaded_video
    )

    file_size_mb = uploaded_video.size / (1024 * 1024)

    st.caption(
        f"File size: {file_size_mb:.2f} MB"
    )


# ============================================================
# EXTRA VIDEO INFORMATION
# ============================================================

st.markdown("---")

st.subheader("📝 Video Information")

video_topic = st.text_input(
    "Video Topic / Idea (Optional)",
    placeholder="Example: Pakistan mein online earning apps"
)

target_audience = st.text_input(
    "Target Audience (Optional)",
    placeholder="Example: Pakistan students, beginners, freelancers"
)

language = st.selectbox(
    "Output Language",
    [
        "Roman Urdu / Hindi",
        "English",
        "Urdu"
    ]
)

video_category = st.selectbox(
    "Video Category",
    [
        "Education",
        "Technology",
        "How-To / Tutorial",
        "Online Earning",
        "Freelancing",
        "News / Updates",
        "Entertainment",
        "Gaming",
        "Review",
        "Other"
    ]
)


# ============================================================
# CREATE PROMPT
# ============================================================

def build_prompt(topic, audience, output_language, category):

    topic_text = topic.strip()

    if not topic_text:
        topic_text = "Analyze the uploaded video and determine its main topic."

    audience_text = audience.strip()

    if not audience_text:
        audience_text = "General YouTube audience"

    prompt = f"""
You are a professional YouTube SEO strategist,
content analyst and YouTube growth consultant.

Analyze the uploaded video carefully.

VIDEO TOPIC / EXTRA INFORMATION:
{topic_text}

TARGET AUDIENCE:
{audience_text}

VIDEO CATEGORY:
{category}

OUTPUT LANGUAGE:
{output_language}

Your job is to understand the actual content of the uploaded video
and create a complete YouTube SEO package based on the video.

IMPORTANT:

- Use information from the uploaded video.
- Do not invent facts.
- Do not create misleading clickbait.
- Titles should be catchy and high-CTR but truthful.
- Description should accurately describe the video.
- Tags should be strongly related to the actual video.
- Hashtags should be relevant.
- Avoid keyword stuffing.
- Make everything easy to copy into YouTube Studio.
- Give practical recommendations rather than guaranteeing virality.

RETURN THESE SECTIONS:

==================================================
1. 🔥 CATCHY YOUTUBE TITLES
==================================================

Give 5 title options.

Make them different from each other.

Try different approaches such as:
- curiosity
- benefit
- problem/solution
- strong keyword
- emotional hook

==================================================
2. 📝 SEO-OPTIMIZED DESCRIPTION
==================================================

Write one complete YouTube description.

Include:
- strong opening hook
- natural keywords
- accurate video summary
- viewer benefit
- call to action

Do not write fake claims.

==================================================
3. 🏷️ YOUTUBE TAGS
==================================================

Give 25 highly relevant YouTube tags.

Return them in one comma-separated line.

==================================================
4. #️⃣ HASHTAGS
==================================================

Give 10 relevant hashtags.

Return them in one line.

==================================================
5. ⏰ BEST UPLOAD TIMING
==================================================

Give practical upload recommendations for Pakistan Standard Time (PKT).

Include:
- best days
- suggested time windows
- audience testing strategy

Important:
Do NOT claim any time guarantees virality.

==================================================
6. 📈 YOUTUBE SEO STRATEGY
==================================================

Give 5 practical tips covering:

1. CTR
2. Search visibility
3. Audience retention
4. Engagement
5. Early video performance

==================================================
7. 🎯 BEST TITLE RECOMMENDATION
==================================================

From your 5 titles, select the single best title
and explain briefly why it is the strongest option.
"""

    return prompt


# ============================================================
# UPLOAD VIDEO TO GEMINI
# ============================================================

def upload_video_to_gemini(client, uploaded_file):

    suffix = Path(uploaded_file.name).suffix

    if not suffix:
        suffix = ".mp4"

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_path = temp_file.name

    try:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_file.close()

        uploaded_gemini_file = client.files.upload(
            file=temp_path
        )

        return uploaded_gemini_file, temp_path

    except Exception:

        try:
            temp_file.close()
        except Exception:
            pass

        raise


# ============================================================
# WAIT FOR VIDEO PROCESSING
# ============================================================

def wait_for_video_processing(client, gemini_file):

    status_placeholder = st.empty()

    while True:

        current_file = client.files.get(
            name=gemini_file.name
        )

        state = getattr(current_file, "state", None)

        if state is None:
            return current_file

        state_name = getattr(
            state,
            "name",
            str(state)
        )

        status_placeholder.info(
            f"🎥 Gemini video processing: {state_name}"
        )

        if state_name == "ACTIVE":
            status_placeholder.success(
                "✅ Video successfully processed by Gemini."
            )
            return current_file

        if state_name in [
            "FAILED",
            "ERROR"
        ]:
            raise RuntimeError(
                f"Gemini video processing failed: {state_name}"
            )

        time.sleep(5)


# ============================================================
# GENERATE SEO CONTENT
# ============================================================

def generate_seo_content(
    api_key_value,
    uploaded_file,
    topic,
    audience,
    output_language,
    category
):

    client = genai.Client(
        api_key=api_key_value
    )

    gemini_file = None
    temporary_path = None

    try:

        # Upload video
        with st.spinner(
            "📤 Video Gemini ko upload ho rahi hai..."
        ):

            gemini_file, temporary_path = upload_video_to_gemini(
                client,
                uploaded_file
            )

        # Wait for processing
        gemini_file = wait_for_video_processing(
            client,
            gemini_file
        )

        # Build prompt
        prompt = build_prompt(
            topic=topic,
            audience=audience,
            output_language=output_language,
            category=category
        )

        # Generate
        with st.spinner(
            "🤖 Gemini video analyze karke SEO content bana raha hai..."
        ):

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    gemini_file,
                    prompt
                ]
            )

        if not response or not response.text:

            raise RuntimeError(
                "Gemini ne empty response return kiya."
            )

        return response.text

    finally:

        # Delete local temporary file
        if temporary_path:

            try:
                os.remove(temporary_path)
            except Exception:
                pass


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown("---")

generate_button = st.button(
    "🚀 Analyze Video & Generate YouTube SEO",
    type="primary",
    use_container_width=True
)


# ============================================================
# GENERATE RESULT
# ============================================================

if generate_button:

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if not api_key.strip():

        st.error(
            "❌ Google AI Studio API key missing hai."
        )

        st.info(
            "Sidebar mein apni Gemini API key paste karein."
        )

    # --------------------------------------------------------
    # API KEY FORMAT CHECK
    # --------------------------------------------------------

    elif not api_key.strip().startswith("AIza"):

        st.error(
            "❌ API key ka format check karein."
        )

        st.info(
            "Google AI Studio ki API key aam tor par "
            "`AIza...` format mein hoti hai."
        )

    # --------------------------------------------------------
    # VIDEO CHECK
    # --------------------------------------------------------

    elif uploaded_video is None:

        st.warning(
            "⚠️ Pehle apni video upload karein."
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    else:

        try:

            result = generate_seo_content(
                api_key_value=api_key.strip(),
                uploaded_file=uploaded_video,
                topic=video_topic,
                audience=target_audience,
                output_language=language,
                category=video_category
            )

            st.success(
                "🎉 Video analysis complete! YouTube SEO package ready hai."
            )

            st.markdown("---")

            st.subheader(
                "🎯 Generated YouTube Content"
            )

            st.markdown(result)

            st.markdown("---")

            # Download text
            st.download_button(
                label="📥 Download SEO Content",
                data=result,
                file_name="youtube_seo_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as error:

            error_message = str(error)

            st.error(
                "❌ Gemini API / Video Processing Error"
            )

            # 401 / 403
            if (
                "401" in error_message
                or "403" in error_message
            ):

                st.warning(
                    "API key invalid, restricted, ya unauthorized ho sakti hai."
                )

                st.info(
                    "Google AI Studio mein apni API key check karein."
                )

            # 404
            elif "404" in error_message:

                st.warning(
                    "Selected Gemini model available nahi hai "
                    "ya API request model ko support nahi kar rahi."
                )

            # 429
            elif "429" in error_message:

                st.warning(
                    "Free-tier rate limit hit ho gayi hai. "
                    "Thori dair baad dobara try karein."
                )

            # Quota
            elif "quota" in error_message.lower():

                st.warning(
                    "Gemini API quota/rate limit issue aa raha hai."
                )

            # Upload issue
            elif (
                "upload" in error_message.lower()
                or "file" in error_message.lower()
            ):

                st.warning(
                    "Video upload/process karne mein problem aayi hai."
                )

            # Generic
            else:

                st.warning(
                    "Request complete nahi ho saki. "
                    "Neeche original error diya gaya hai."
                )

            st.code(
                error_message
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎬 AI Viral Video Studio | Streamlit + Google Gemini"
)
```

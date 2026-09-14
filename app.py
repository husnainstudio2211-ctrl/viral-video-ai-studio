import streamlit as st
from google import genai

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Viral Video Studio",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("🎬 AI Viral Video Studio")

st.markdown(
    "YouTube creators ke liye AI-powered Titles, Descriptions, "
    "Tags, Hashtags aur Upload Strategy generator."
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔑 Gemini API Setup")

api_key = st.sidebar.text_input(
    "Google AI Studio API Key",
    type="password",
    placeholder="AIza..."
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Google AI Studio se apni Gemini API key paste karein."
)

# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.1-flash-lite"

# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("📝 Video Details")

video_topic = st.text_area(
    "Video Topic / Idea",
    placeholder="Example: How to earn money online from Pakistan",
    height=120
)

target_audience = st.text_input(
    "Target Audience (Optional)",
    placeholder="Example: Pakistan students, beginners, freelancers"
)

language = st.selectbox(
    "Output Language",
    [
        "English",
        "Roman Urdu / Hindi",
        "Urdu"
    ]
)

video_category = st.selectbox(
    "Video Category",
    [
        "Education",
        "Technology",
        "How-To / Tutorial",
        "Entertainment",
        "Gaming",
        "News / Updates",
        "Online Earning",
        "Freelancing",
        "Other"
    ]
)

# ============================================================
# PROMPT
# ============================================================

def create_prompt(topic, audience, output_language, category):

    audience_text = audience.strip()

    if not audience_text:
        audience_text = "General YouTube audience"

    return f"""
You are a professional YouTube SEO strategist and content expert.

Create a complete YouTube SEO package for this video.

VIDEO TOPIC:
{topic}

TARGET AUDIENCE:
{audience_text}

VIDEO CATEGORY:
{category}

OUTPUT LANGUAGE:
{output_language}

Your goal is to help the creator improve click-through rate,
search discoverability, viewer interest and engagement.

IMPORTANT RULES:

- Do not use fake or misleading clickbait.
- Titles should be catchy but truthful.
- Descriptions should be natural and SEO optimized.
- Tags must be directly relevant to the video topic.
- Hashtags must be relevant.
- Do not keyword stuff.
- Do not invent facts.
- Make the output easy to copy into YouTube Studio.

RETURN EXACTLY THESE SECTIONS:

1. CATCHY TITLES
Give 5 different YouTube title options.

2. SEO DESCRIPTION
Write one complete YouTube description.
Include:
- strong opening hook
- natural keywords
- video summary
- viewer benefit
- call to action

3. YOUTUBE TAGS
Give 25 relevant tags.
Put them in one comma-separated line.

4. HASHTAGS
Give 10 relevant hashtags.
Put them in one line.

5. BEST UPLOAD TIMING
Give practical upload timing suggestions for Pakistan Standard Time (PKT).
Include:
- best days
- best time windows
- testing strategy

Do not claim that a specific upload time guarantees virality.

6. SEO STRATEGY
Give 5 practical tips for:
- CTR
- search visibility
- retention
- engagement
- early performance
"""

# ============================================================
# GENERATE CONTENT
# ============================================================

if st.button(
    "🚀 Generate YouTube SEO",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not api_key.strip():

        st.error(
            "❌ Pehle sidebar mein Google AI Studio API key enter karein."
        )

    elif not api_key.strip().startswith("AIza"):

        st.error(
            "❌ API key ka format check karein. "
            "Google AI Studio key aam tor par AIza... se start hoti hai."
        )

    elif not video_topic.strip():

        st.warning(
            "⚠️ Pehle apni video ka topic ya idea enter karein."
        )

    else:

        try:

            # ------------------------------------------------
            # CREATE GEMINI CLIENT
            # ------------------------------------------------

            client = genai.Client(
                api_key=api_key.strip()
            )

            prompt = create_prompt(
                topic=video_topic.strip(),
                audience=target_audience,
                output_language=language,
                category=video_category
            )

            # ------------------------------------------------
            # GEMINI REQUEST
            # ------------------------------------------------

            with st.spinner(
                "🤖 Gemini AI aapka YouTube SEO package bana raha hai..."
            ):

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            if response and response.text:

                st.success(
                    "✅ YouTube SEO content successfully generated!"
                )

                st.markdown("---")

                st.subheader("🎯 Your YouTube SEO Package")

                st.markdown(response.text)

                # --------------------------------------------
                # DOWNLOAD
                # --------------------------------------------

                st.download_button(
                    label="📥 Download SEO Content",
                    data=response.text,
                    file_name="youtube_seo_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            else:

                st.error(
                    "❌ Gemini ne koi text response return nahi kiya."
                )

        except Exception as error:

            error_message = str(error)

            st.error("❌ Gemini API Error")

            # ----------------------------------------------
            # ERROR HELP
            # ----------------------------------------------

            if "404" in error_message:

                st.warning(
                    "Model/API endpoint issue aa raha hai. "
                    "Code mein current Gemini model use ho raha hai."
                )

            elif "401" in error_message or "403" in error_message:

                st.warning(
                    "API key invalid, restricted, ya unauthorized ho sakti hai. "
                    "Google AI Studio mein apni key check karein."
                )

            elif "429" in error_message:

                st.warning(
                    "Free-tier rate limit hit ho gayi hai. "
                    "Baad mein dobara try karein."
                )

            elif "quota" in error_message.lower():

                st.warning(
                    "API quota/rate limit issue aa raha hai."
                )

            else:

                st.warning(
                    "API request mein problem aa gayi hai. "
                    "Neeche original error diya gaya hai."
                )

            st.code(error_message)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🎬 AI Viral Video Studio | Streamlit + Google Gemini"
)

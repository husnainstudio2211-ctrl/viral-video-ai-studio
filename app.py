```python
import os
import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AI Viral Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 18px;
            color: #666;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 700;
            margin-top: 15px;
        }

        .result-box {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            background-color: rgba(128,128,128,0.06);
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">🎬 AI Viral Video Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'YouTube ke liye Titles, Descriptions, Tags, Hashtags aur Upload Strategy generate karein.'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.header("🔑 Gemini Configuration")

# Try environment variable first
env_api_key = os.getenv("GEMINI_API_KEY", "")

api_key = st.sidebar.text_input(
    "Google AI Studio API Key",
    value=env_api_key,
    type="password",
    placeholder="AIza..."
)

st.sidebar.markdown("---")

st.sidebar.subheader("🤖 Gemini Model")

model_options = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]

selected_model = st.sidebar.selectbox(
    "Model select karein:",
    model_options,
    index=0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Google AI Studio se API key banai ja sakti hai. "
    "Free tier ki usage limits hoti hain."
)

# =========================================================
# MAIN INPUTS
# =========================================================
st.markdown(
    '<div class="section-title">📝 Video Details</div>',
    unsafe_allow_html=True
)

video_topic = st.text_area(
    "Video Topic / Idea",
    placeholder=(
        "Example: How to earn money online from Pakistan using freelancing apps"
    ),
    height=120
)

target_audience = st.text_input(
    "Target Audience (Optional)",
    placeholder="Example: Pakistan beginners, students, freelancers"
)

video_language = st.selectbox(
    "Content Language",
    [
        "Roman Urdu / Hindi",
        "English",
        "Urdu"
    ]
)

video_type = st.selectbox(
    "Video Type",
    [
        "Informational",
        "Tutorial / How-To",
        "News / Updates",
        "Review",
        "Story / Entertainment",
        "Educational",
        "Gaming",
        "Technology"
    ]
)

# =========================================================
# GENERATION FUNCTION
# =========================================================
def generate_youtube_seo(
    api_key_value,
    model_name,
    topic,
    audience,
    language,
    content_type
):
    """
    Generate YouTube SEO package using the Google GenAI SDK.
    """

    client = genai.Client(api_key=api_key_value)

    audience_text = audience.strip() if audience.strip() else "General audience"

    prompt = f"""
You are an expert YouTube SEO strategist, content strategist,
CTR specialist and YouTube growth consultant.

Create a professional YouTube SEO package for this video.

VIDEO TOPIC:
{topic}

TARGET AUDIENCE:
{audience_text}

LANGUAGE:
{language}

VIDEO TYPE:
{content_type}

IMPORTANT GOALS:
- Make titles highly clickable without fake clickbait.
- Make the description naturally SEO optimized.
- Use relevant search keywords.
- Do not keyword-stuff.
- Tags should be directly related to the topic.
- Hashtags should be relevant and useful.
- Upload timing should be presented as a practical recommendation,
  not as a guaranteed viral result.
- Do not invent facts about the topic.
- Keep everything useful for a real YouTube creator.

OUTPUT FORMAT:

## 1. 🔥 CATCHY TITLES
Give exactly 5 title options.

For each title:
- Keep it natural.
- Focus on CTR.
- Make each option different.

## 2. 📝 SEO DESCRIPTION
Write one professional YouTube description containing:
- Strong opening hook
- Clear topic summary
- Relevant keywords
- Natural SEO language
- Viewer value
- Call to action

## 3. 🏷️ YOUTUBE TAGS
Give 20-30 highly relevant tags.
Return them in one comma-separated line.

## 4. #️⃣ HASHTAGS
Give 10 relevant hashtags.
Return them in one line.

## 5. ⏰ BEST UPLOAD TIMING
Give:
- Recommended days
- Recommended time windows
- Pakistan Standard Time (PKT) guidance
- A short explanation
- Simple strategy for testing upload times

## 6. 📈 EXTRA SEO STRATEGY
Give 5 practical tips that can improve:
- CTR
- Search discoverability
- Retention
- Engagement
- Early video performance

Make the answer clean and easy to copy into YouTube Studio.
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    if not response or not response.text:
        raise RuntimeError("Gemini ne empty response return kiya.")

    return response.text


# =========================================================
# BUTTON
# =========================================================
generate_button = st.button(
    "🚀 Generate Viral YouTube SEO",
    type="primary",
    use_container_width=True
)

# =========================================================
# GENERATE
# =========================================================
if generate_button:

    if not api_key.strip():
        st.error("❌ Sab se pehle Google AI Studio API Key enter karein.")

    elif not api_key.strip().startswith("AIza"):
        st.warning(
            "⚠️ API key aam tor par AI Studio key ki tarah `AIza...` "
            "se start hoti hai. Key ko dobara check karein."
        )

    elif not video_topic.strip():
        st.warning("⚠️ Video topic/idea zaroor enter karein.")

    else:

        try:
            with st.spinner(
                f"🤖 {selected_model} se YouTube SEO content generate ho raha hai..."
            ):

                result = generate_youtube_seo(
                    api_key_value=api_key.strip(),
                    model_name=selected_model,
                    topic=video_topic.strip(),
                    audience=target_audience,
                    language=video_language,
                    content_type=video_type
                )

            st.success("✅ YouTube SEO package successfully generate ho gaya!")

            st.markdown("---")

            # =================================================
            # RESULTS
            # =================================================
            st.markdown(
                '<div class="section-title">🎯 Generated Content</div>',
                unsafe_allow_html=True
            )

            st.markdown(result)

            # =================================================
            # DOWNLOAD
            # =================================================
            st.markdown("---")

            st.download_button(
                label="📥 Download SEO Content",
                data=result,
                file_name="youtube_seo_content.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            error_text = str(e)

            st.error("❌ Gemini API Error")

            # Helpful error messages
            if "404" in error_text and "not found" in error_text.lower():
                st.warning(
                    "Model available nahi hai. Sidebar mein doosra model select "
                    "karke دوبارہ try karein."
                )

            elif "401" in error_text or "403" in error_text:
                st.warning(
                    "API key invalid ya unauthorized lag rahi hai. "
                    "Google AI Studio mein key check karein."
                )

            elif "429" in error_text:
                st.warning(
                    "Free-tier rate limit hit ho gayi hai. "
                    "Thori dair baad دوبارہ try karein."
                )

            elif "quota" in error_text.lower():
                st.warning(
                    "API quota/rate limit issue aa raha hai. "
                    "Apni AI Studio usage check karein."
                )

            st.code(error_text)


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "🎬 AI Viral Video Studio • Powered by Google Gemini API • Streamlit"
)
```

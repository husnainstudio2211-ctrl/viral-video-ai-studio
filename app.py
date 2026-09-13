from io import BytesIO
import os
import tempfile
import time
import cv2
from google import genai
from gtts import gTTS
from PIL import Image
import streamlit as st

# Safe API Key handling for Local & Streamlit Cloud
try:
  API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
  API_KEY = "AQ.Ab8RN6KEZlh_BvE_TpY0cCc1b6RceQ4EBNLl2gz5sKwR-yXvug"

client = genai.Client(api_key=API_KEY)


# Video ke andar se REAL frames nikalne ka function
def extract_real_video_frames(video_path, num_frames=3):
  cap = cv2.VideoCapture(video_path)
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  extracted_images = []

  if total_frames > 0:
    positions = [
        int(total_frames * 0.20),
        int(total_frames * 0.50),
        int(total_frames * 0.80),
    ]
    for pos in positions[:num_frames]:
      cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
      ret, frame = cap.read()
      if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        extracted_images.append(img)
  cap.release()
  return extracted_images


# Resolution & Quality Resize Function
def process_image_quality(img, option):
  img_copy = img.copy()

  if option == "Small / Low KB (Compressed)":
    img_copy.thumbnail((640, 360), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img_copy.save(buf, format="JPEG", quality=35)
    return buf.getvalue(), "image/jpeg", "jpg"

  elif option == "1080p (Full HD)":
    aspect = img_copy.width / img_copy.height
    new_w = int(1080 * aspect)
    img_resized = img_copy.resize((new_w, 1080), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img_resized.save(buf, format="PNG")
    return buf.getvalue(), "image/png", "png"

  elif option == "4K (Ultra HD)":
    aspect = img_copy.width / img_copy.height
    new_w = int(2160 * aspect)
    img_resized = img_copy.resize((new_w, 2160), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img_resized.save(buf, format="PNG")
    return buf.getvalue(), "image/png", "png"

  elif option == "8K (Ultra HD)":
    aspect = img_copy.width / img_copy.height
    new_w = int(4320 * aspect)
    img_resized = img_copy.resize((new_w, 4320), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img_resized.save(buf, format="PNG")
    return buf.getvalue(), "image/png", "png"

  else:  # Original Quality
    buf = BytesIO()
    img_copy.save(buf, format="PNG")
    return buf.getvalue(), "image/png", "png"


# Streamlit App Config
st.set_page_config(page_title="My Viral Video AI Studio", layout="wide")
st.title("🎬 My Viral Video AI Studio")

uploaded_file = st.file_uploader(
    "Apni video upload karein (.mp4, .mov)", type=["mp4", "mov", "avi"]
)

if uploaded_file is not None:
  if (
      "last_uploaded_file" in st.session_state
      and st.session_state.last_uploaded_file != uploaded_file.name
  ):
    if "processed_data" in st.session_state:
      del st.session_state["processed_data"]
  st.session_state.last_uploaded_file = uploaded_file.name

  st.video(uploaded_file)

  # Process Button
  if st.button("🚀 Process Video & Extract Real Thumbnails"):
    with st.spinner(
        "⚡ Fast Processing: Extracting Real Frames & Viral SEO Metadata..."
    ):

      with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        video_path = tmp.name

      try:
        # 1. Real Frames Capture (Instant)
        real_frames = extract_real_video_frames(video_path)

        # 2. Google Gemini API Upload
        video_file = client.files.upload(file=video_path)

        while video_file.state.name == "PROCESSING":
          time.sleep(1)
          video_file = client.files.get(name=video_file.name)

        if video_file.state.name == "FAILED":
          st.error("Video processing fail ho gayi!")
        else:
          prompt = """
                    Aap ek world-class Viral Content Specialist hain. Is video ke EXACT AUDIO aur VISUAL TOPIC ko dhyan se samajhein.

                    Video ke EXACT content par mabni Roman Urdu / Hindi mein ye high-converting details dein:

                    🔥 **1. Top 3 High CTR Viral Titles:**
                    - Video ke exact topic par mabni 3 aise catchy titles jo har koi click karne par majboor ho jaye.

                    📌 **2. Thumbnail / Screen Overlay Taglines:**
                    - 3 Short & Punchy taglines (2-4 words) jo screen ya thumbnail par likhi ja sakein.

                    📝 **3. High Converting Video Description:**
                    - Complete viral post description (Hook + Main Value + Call-to-Action).

                    🏷️ **4. SEO Tags & Video Keywords:**
                    - Comma-separated high-volume search tags for YouTube/TikTok search ranking.

                    #️⃣ **5. Top 15 Viral Hashtags:**
                    - Exact video topic se related trending hashtags (#OnlineEarning #EarnMoneyOnline etc. agar online earning ho).

                    ⏰ **6. Best Posting Schedule & Platform:**
                    - Platform (Shorts, Reels, TikTok) aur sabse best posting time.

                    💡 **7. Quick Viral Audit & Improvement Tip:**
                    - 2 Lines mein audio/video lighting aur hook ka exact review.
                    """

          response = client.models.generate_content(
              model="gemini-3.6-flash", contents=[video_file, prompt]
          )
          full_text = response.text

          # Fast TTS Audio Summary
          audio_bytes = None
          try:
            clean_speech_text = (
                full_text.replace("*", "").replace("#", "").replace("[", "")
            )
            tts = gTTS(text=clean_speech_text[:500], lang="hi")
            audio_buf = BytesIO()
            tts.write_to_fp(audio_buf)
            audio_bytes = audio_buf.getvalue()
          except Exception:
            pass

          # 💾 Permanent Session Memory Save
          st.session_state.processed_data = {
              "real_frames": real_frames,
              "full_text": full_text,
              "audio_bytes": audio_bytes,
          }

        client.files.delete(name=video_file.name)
      finally:
        if os.path.exists(video_path):
          os.remove(video_path)

  # 📌 Display Saved Results
  if "processed_data" in st.session_state:
    data = st.session_state.processed_data
    real_frames = data["real_frames"]
    full_text = data["full_text"]
    audio_bytes = data["audio_bytes"]

    st.success("✅ Fast Analysis Complete!")

    # 🖼️ REAL VIDEO THUMBNAILS WITH QUALITY SELECTOR
    st.subheader("🖼️ Asli Video Frames (Download in Low KB / 4K / 8K)")
    if real_frames:
      cols = st.columns(len(real_frames))
      for idx, (col, img) in enumerate(zip(cols, real_frames)):
        with col:
          st.image(
              img, caption=f"Real Frame {idx+1}", use_container_width=True
          )

          selected_quality = st.selectbox(
              f"Select Quality (Frame {idx+1}):",
              [
                  "Original Quality",
                  "Small / Low KB (Compressed)",
                  "1080p (Full HD)",
                  "4K (Ultra HD)",
                  "8K (Ultra HD)",
              ],
              key=f"quality_select_{idx}",
          )

          img_data, mime_type, file_ext = process_image_quality(
              img, selected_quality
          )

          st.download_button(
              label=f"📥 Download ({selected_quality})",
              data=img_data,
              file_name=f"real_thumbnail_{idx+1}_{selected_quality.replace(' ', '_')}.{file_ext}",
              mime=mime_type,
              key=f"dl_btn_{idx}",
          )

    # 🔊 Quick Audio Voice Summary
    st.subheader("🔊 Quick Voice Summary (Suniye)")
    if audio_bytes:
      st.audio(audio_bytes, format="audio/mp3")

    # Display Text Analysis
    st.markdown(full_text)

    # Reset Button
    if st.button("🗑️ Clear Results & Reset"):
      del st.session_state["processed_data"]
      st.rerun()

else:
  if "processed_data" in st.session_state:
    del st.session_state["processed_data"]
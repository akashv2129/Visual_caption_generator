import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature": 0.7},
)

# ======================= Custom CSS ===========================
st.set_page_config(page_title="🌈 Image Caption Generator", layout="wide")
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
    }
    .stApp {
        background: linear-gradient(to top left, #a1c4fd 0%, #c2e9fb 100%);
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        padding: 2rem;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff6a00, #ee0979);
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        border-radius: 10px;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #ee0979, #ff6a00);
        transform: scale(1.05);
        cursor: pointer;
    }
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
    }
    .caption-box {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 1rem;
        border-radius: 12px;
        margin-top: 1rem;
        font-size: 1.2rem;
        color: #1a1a1a;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ======================= App Layout ===========================
st.markdown("# ✨ Image Caption Generator")
st.markdown("Upload an image and let Gemini describe it in a poetic or descriptive way!")

uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image.thumbnail((400, 400))

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(image, caption="🖼 Preview", width=300)

    with col2:
        # Caption style selector
        style = st.radio(
            "🎭 Choose Caption Style:",
            ["Descriptive (Normal)", "Poetic (4-line)"]
        )

        if st.button("🎨 Generate Caption"):
            with st.spinner("🧠 Thinking..."):
                try:
                    # Adjust prompt based on selected style
                    if style == "Poetic (4-line)":
                        prompt = (
                            "Generate a four-line poetic and natural caption for this image. "
                            "Describe the visible people, objects, and scenery in a gentle and artistic tone."
                        )
                    else:
                        prompt = (
                            "Generate a simple, clear, and accurate one-sentence caption for this image. "
                            "Avoid poetic or flowery language. Focus on what is directly visible in the image."
                        )

                    response = model.generate_content([prompt, image])
                    caption = response.text.strip()

                    st.success("✅ Caption Generated")
                    st.markdown(f"<div class='caption-box'>{caption}</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
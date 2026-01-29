import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pandas as pd
import os

font_path = os.path.abspath("Alice-Regular.ttf") #times new roman font
# Load logo image
logo = Image.open("NSS.png").resize((150, 150))
st.set_page_config(page_title="DJS NSS Event", page_icon=logo)

simple_css = """
    <style>
    .stApp {
        background: linear-gradient(to right, #2563eb, #06b6d4) !important;
        min-height: 100vh;
        overflow-y: auto;
        scroll-behavior: smooth;
    }
    .custom-title {
        color: #fff;
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        animation: fadeIn 1.5s ease-in-out;
        margin-top: 20px;
    }
    .stTextInput input {
        font-size: 18px !important;
        padding: 12px !important;
        text-align: center !important;
        color: black !important;
        background: white !important;
        border: 2px solid #2563eb !important;
        border-radius: 8px !important;
        outline: none !important;
        caret-color: #2563eb !important; /* blue cursor */
        transition: box-shadow 0.2s;
    }
    .stTextInput input:focus {
        box-shadow: 0 0 0 2px #06b6d4 !important;
        border-color: #06b6d4 !important;
    }
    .stSelectbox [data-baseweb="select"] {
        color: black !important;
    }
    .stSelectbox [data-baseweb="select"] * {
        color: black !important;
        background: white !important;
    }
    .stButton>button {
        background: #fff;
        color: #4a6fa5;
        font-size: 22px;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: #e0eafc;
        color: #4a6fa5;
    }
    .stSuccess, .stWarning {
        position: relative;
        z-index: 2;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        margin-top: 15px;
        font-weight: bold;
    }
    .stSuccess {
        background-color: #8ec7ab !important;
        color: white !important;
    }
    .stWarning {
        background-color: #e7816d !important;
        color: white !important;
    }
    </style>
"""
st.markdown(simple_css, unsafe_allow_html=True)
# Map display names to file-safe names
EVENTS = {
     "NSS Camp 2026": "nss_camp_2026",
}

# Add per-event relative positions (fractions of width/height).
POSITIONS = {
    "nss_camp_2026": {
        "name": (0.50, 0.38),      # centered horizontally, 40% down from top
    },
}

def get_attendee_quantity(name, event_display):
    """
    Return True if `name` is found in the event CSV, else None.
    """
    event_key = EVENTS[event_display]
    csv_path = f"attendance/{event_key}.csv"
    try:
        df = pd.read_csv(csv_path)
        # find a Name-like column (case-insensitive)
        name_cols = [c for c in df.columns if c.strip().lower() == "name"]
        if not name_cols:
            return None
        name_col = name_cols[0]
        df["Name_norm"] = df[name_col].astype(str).str.strip().str.lower()
        name_norm = name.strip().lower()
        matched = df[df["Name_norm"] == name_norm]
        if matched.empty:
            return None
        return True
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

def overlay_name_on_template(name, event_display, quantity=None):
    event_key = EVENTS[event_display]
    template_path = f"templates/{event_key}.jpg"
    template_img = Image.open(template_path)
    draw = ImageDraw.Draw(template_img)

    img_width, img_height = template_img.size

    # lookup positions (fallback to centered)
    pos = POSITIONS.get(event_key, {})
    name_rel = pos.get("name", (0.5, 0.5))

    name_x = int(img_width * name_rel[0])
    name_y = int(img_height * name_rel[1])

    # Draw name
    font_name = ImageFont.truetype(font_path, 120)
    draw.text((name_x, name_y), name, fill=(0, 0, 0), anchor="mm", align="center", font=font_name)

    return template_img

def generate_pdf_with_image(name, event_display, quantity=None):
    img_with_overlay = overlay_name_on_template(name, event_display)
    img_buffer = io.BytesIO()
    img_with_overlay.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(img_with_overlay.width, img_with_overlay.height))
    img = ImageReader(img_buffer)
    c.drawImage(img, 0, 0, width=img_with_overlay.width, height=img_with_overlay.height)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def main():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo, width=120)
    with col2:
        st.markdown('<div class="custom-title">DJS NSS Certificates</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("Enter your full name:", key="name_input").strip().title()
    email_input = st.text_input("Enter your email:", key="email_input").strip()
    event_display = st.selectbox("Select Event", list(EVENTS.keys()))
    
    if st.button("Generate Certificate"):
        if user_input and email_input:
            found = get_attendee_quantity(user_input, event_display)
            if not found:
                st.warning(f"⚠️ Name not found in the attendance list for {event_display}.")
                return
            img_with_overlay = overlay_name_on_template(user_input, event_display)
            st.image(img_with_overlay, caption="Generated Certificate", use_container_width=True)            
            pdf_buffer = generate_pdf_with_image(user_input, event_display)
            st.success("📨 You can download your certificate.")
            # Download button for PDF
            st.download_button(
                label="Download Certificate as PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"{user_input}_{event_display}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ Please enter a valid name and email.")

if __name__ == "__main__":
    main()

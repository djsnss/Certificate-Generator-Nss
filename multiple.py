import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Load logo image
logo = Image.open("NSS.png").resize((200, 200))
st.set_page_config(page_title="DJS NSS Event", page_icon=logo)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #a8e6ff, #ffeb99);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .stButton>button {
        text-align: center;
        display: block;
        margin: auto;
    }
    .stTextInput>div>div>input {
        background-color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
        text-align: center;
        border: 1px solid #0077b6;
        color: black;
    }
    .stTextInput>label {
        color: black !important;
        font-size: 36px !important;
        font-weight: 500 !important;
    }
    .stSelectbox>label {
        color: black !important;
        font-size: 36px !important;
        font-weight: 500 !important;
    }
    .custom-title {
        font-family: 'Arial', sans-serif;
        color: #003366;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-top: 20px;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .custom-text {
        font-family: 'Arial', sans-serif;
        color: black;
        font-size: 18px;
        margin-top: 10px;
        text-align: center;
        opacity: 0.9;
    }
    .stWarning {
        background-color: rgba(0, 119, 182, 0.3) !important;
        color: #000000 !important;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    .stSuccess {
        background-color: rgba(28, 200, 28, 0.3) !important;
        color: #006400 !important;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
        margin-bottom: 20px;  /* Added space below the success message */
    }
    </style>
""", unsafe_allow_html=True)

def get_font(size=175):
    """Try to load font with fallbacks"""
    try:
        return ImageFont.truetype("playlist script.otf", size)  # Custom font
    except OSError:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except OSError:
            try:
                return ImageFont.truetype("DejaVuSans.ttf", size)
            except OSError:
                return ImageFont.load_default()

def overlay_name_on_template(name, event):
    """Generate a certificate with the user's name"""
    templates = {
        "NSS Camp 2025": "templates/camp.jpg",  
        "Stem Cell Donation Drive": "templates/stemcell.jpg",  
        "Grain-a-thon 2.0": "templates/grainathon.jpg",   
        "Participation": "templates/various.jpg"
    }

    template_img = Image.open(templates.get(event, "templates/various.jpg"))  
    draw = ImageDraw.Draw(template_img)
    font = get_font(80)  
    
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    img_width, img_height = template_img.size
    x = (img_width - text_width) / 2
    
    if event == "Participation":
        y = (img_height - text_height) / 2 - 140  # Move text more up for Participation
    else:
        y = (img_height - text_height) / 2 - 80 
    
    draw.text((x, y), name, fill=(0, 0, 0), font=font)
    return template_img

def generate_pdf_with_image(name, event):
    """Generate a PDF that includes the certificate image based on the event"""
    img_with_overlay = overlay_name_on_template(name, event)

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
        st.image(logo, width=125)
    with col2:
        st.markdown('<div class="custom-title">DJS NSS Event</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("What is your full name?", key="name_input").strip().title()
    event = st.selectbox("Select Event", ["NSS Camp 2025", "Stem Cell Donation Drive", "Grain-a-thon 2.0", "Participation"])
    
    st.markdown('<div class="custom-text">Please input your name and select an event above. Thank you!</div>', unsafe_allow_html=True)
    
    if st.button("Generate Certificate"):
        if user_input:
            img_with_overlay = overlay_name_on_template(user_input, event)
            st.image(img_with_overlay, caption="Generated Certificate", use_container_width=True)
            
            pdf_buffer = generate_pdf_with_image(user_input, event)
            st.markdown('<div class="stSuccess">Certificate preview generated successfully!</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="Download Certificate PDF",
                data=pdf_buffer,
                file_name=f"{user_input}_{event}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.markdown('<div class="stWarning">Please enter a valid name.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

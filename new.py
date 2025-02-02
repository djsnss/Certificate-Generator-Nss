import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Load logo image
logo = Image.open("NSS.png").resize((150, 150))
st.set_page_config(page_title="DJS NSS Event", page_icon=logo)

# Inject animated background HTML
st.markdown("""
    <div class="area">
        <ul class="circles">
            <li></li><li></li><li></li><li></li><li></li>
            <li></li><li></li><li></li><li></li><li></li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Custom CSS with previous styling
temp_css = """
    <style>
    @import url('https://fonts.googleapis.com/css?family=Exo:400,700');
    
    * { margin: 0; padding: 0; }
    body { font-family: 'Exo', sans-serif; }
    
    .stApp {
        background: linear-gradient(to left, #e0eafc, #cfdef3);
        min-height: 100vh;
    }
    
    .custom-title {
        color: #4a6fa5;
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(74, 111, 165, 0.2);
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: white;
        border-radius: 20px;
        font-size: 18px;
        padding: 12px;
        text-align: center;
        border: 2px solid #a4c1e4;
        color: #4a6fa5;
        transition: 0.3s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #7ea3d7 !important;
        box-shadow: 0px 0px 15px rgba(126, 163, 215, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #7ea3d7, #a4c1e4);
        color: white;
        font-size: 22px;
        padding: 15px 25px;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a4c1e4, #7ea3d7);
        transform: scale(1.05);
    }
    </style>
"""
st.markdown(temp_css, unsafe_allow_html=True)

def get_font(size=80):
    try:
        return ImageFont.truetype("playlist script.otf", size)
    except OSError:
        return ImageFont.truetype("arial.ttf", size)

def overlay_name_on_template(name, event):
    templates = {
        "NSS Camp 2025": "camp.jpg",  
        "Stem Cell Donation Drive": "stemcell.jpg",  
        "Grain-a-thon 2.0": "grainathon.jpg",   
        "Participation": "various.jpg"
    }
    template_img = Image.open(templates.get(event, "various.jpg"))  
    draw = ImageDraw.Draw(template_img)
    font = get_font(80)
    
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    img_width, img_height = template_img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2 - 80
    
    draw.text((x, y), name, fill=(0, 0, 0), font=font)
    return template_img

def generate_pdf_with_image(name, event):
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
        st.image(logo, width=120)
    with col2:
        st.markdown('<div class="custom-title">DJS NSS Event</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("Enter your full name:", key="name_input").strip().title()
    event = st.selectbox("Select Event", ["NSS Camp 2025", "Stem Cell Donation Drive", "Grain-a-thon 2.0", "Participation"])
    
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

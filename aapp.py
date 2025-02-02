import streamlit as st
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        background-color: #0077b6;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
        transition: background-color 0.3s;
        border: none;
        text-align: center;
        display: block;
        margin: auto;
    }
    .stButton>button:hover {
        background-color: #005f87;
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
    div[data-baseweb="notification"] {
        background-color: rgba(0, 119, 182, 0.3) !important;
    }
    .stWarning > div {
        background-color: rgba(0, 119, 182, 0.3) !important;
    }
    .stWarning p {
        color: #000000 !important;
    }
    .stSuccess {
        color: black !important;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        max-width: 600px;
        width: 100%;
        text-align: center;
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

def overlay_name_on_template(name):
    """Generate a certificate with the user's name"""
    template_img = Image.open("certificate_template.jpg")  # Use your certificate template image here
    draw = ImageDraw.Draw(template_img)
    font = get_font(100)  # Use the custom font with appropriate size
    
    # Get text size and calculate position
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    img_width, img_height = template_img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2 - 80  # Move the text 100px up
    
    # Draw the name on the template with black text (no border)
    draw.text((x, y), name, fill=(0, 0, 0), font=font)
    return template_img

def generate_pdf(name):
    """Generate a certificate in PDF format with the user's name"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Create a placeholder template (use a real template if needed)
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, letter[0], letter[1], fill=1)

    # Add the name in the center
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(200, 400, f"{name}")

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
    st.markdown('<div class="custom-text">Please input your name in the above field. Thank you!</div>', unsafe_allow_html=True)
    
    if st.button("Generate Certificate"):
        if user_input:
            # Generate the certificate image
            img_with_overlay = overlay_name_on_template(user_input)
            # Display the generated image with the certificate
            st.image(img_with_overlay, caption="Generated Certificate", use_container_width=True)
            
            # Generate the PDF
            pdf_buffer = generate_pdf(user_input)
            st.success("Certificate preview generated!")
            
            # Provide download button for PDF
            st.download_button(
                label="Download Certificate PDF",
                data=pdf_buffer,
                file_name="certificate.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Please enter a valid name.")

if __name__ == "__main__":
    main()

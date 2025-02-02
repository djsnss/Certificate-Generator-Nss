import streamlit as st
import io
import smtplib
from email.message import EmailMessage
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pandas as pd
import os
print(os.path.exists("playlist script.otf"))

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
        animation: fadeIn 1.5s ease-in-out; /* Added animation */
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        font-size: 18px;
        padding: 12px;
        text-align: center;
        color: #4a6fa5;
        transition: 0.3s ease-in-out; /* Added transition */
    }
    .stTextInput>div>div>input:focus {
        border-color: #7ea3d7 !important;
        box-shadow: 0px 0px 15px rgba(126, 163, 215, 0.3);
    }
    
    .stSelectbox>label {
        color: #4a6fa5 !important;
        font-size: 22px !important;
        font-weight: 700 !important;
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
        transition: all 0.3s ease-in-out; /* Added transition */
        box-shadow: 2px 2px 10px rgba(126, 163, 215, 0.3); /* Added box shadow */
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a4c1e4, #7ea3d7);
        transform: scale(1.05);
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
        background-color: rgba(142, 199, 171, 1) !important;
        color: white !important;
        box-shadow: 0px 0px 10px rgba(142, 199, 171, 0.8);
    }

    .stWarning {
        background-color: rgba(231, 129, 109, 1) !important;
        color: white !important;
        box-shadow: 0px 0px 10px rgba(231, 129, 109, 0.8);
    }

        /* Animation area */
    .area {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 1;
    }

    /* Override Streamlit's background with softer gradient */
    .stApp {
        background: #e0eafc;  
        background: -webkit-linear-gradient(to left, #e0eafc, #cfdef3);  
        background: linear-gradient(to left, #e0eafc, #cfdef3); 
    }

    /* Animated circles */
    .circles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }

    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.8);  /* Lighter, more subtle circles */
        animation: animate 25s linear infinite;
        bottom: -150px;
    }

    .circles li:nth-child(1) {
        left: 25%;
        width: 80px;
        height: 80px;
        animation-delay: 0s;
    }

    .circles li:nth-child(2) {
        left: 10%;
        width: 20px;
        height: 20px;
        animation-delay: 2s;
        animation-duration: 12s;
    }

    .circles li:nth-child(3) {
        left: 70%;
        width: 20px;
        height: 20px;
        animation-delay: 4s;
    }

    .circles li:nth-child(4) {
        left: 40%;
        width: 60px;
        height: 60px;
        animation-delay: 0s;
        animation-duration: 18s;
    }

    .circles li:nth-child(5) {
        left: 65%;
        width: 20px;
        height: 20px;
        animation-delay: 0s;
    }

    .circles li:nth-child(6) {
        left: 75%;
        width: 110px;
        height: 110px;
        animation-delay: 3s;
    }

    .circles li:nth-child(7) {
        left: 35%;
        width: 150px;
        height: 150px;
        animation-delay: 7s;
    }

    .circles li:nth-child(8) {
        left: 50%;
        width: 25px;
        height: 25px;
        animation-delay: 15s;
        animation-duration: 45s;
    }

    .circles li:nth-child(9) {
        left: 20%;
        width: 15px;
        height: 15px;
        animation-delay: 2s;
        animation-duration: 35s;
    }

    .circles li:nth-child(10) {
        left: 85%;
        width: 150px;
        height: 150px;
        animation-delay: 0s;
        animation-duration: 11s;
    }


    @keyframes animate {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
            border-radius: 0;
        }
        100% {
            transform: translateY(-1000px) rotate(720deg);
            opacity: 0;
            border-radius: 50%;
        }
    }

    /* Content Styling */
    .stTextInput,
    .stSelectbox,
    .stButton,
    .custom-title,
    img {
        position: relative;
        z-index: 2;
    }

    /* Custom Title with updated color */
    .custom-title {
        color: #4a6fa5;  /* Softer blue color for title */
        font-size: 50px;
        font-weight: 800;
        margin-top: 20px;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(74, 111, 165, 0.2);
        animation: fadeIn 1.5s ease-in-out;
    }

    /* Input Fields with updated colors */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        font-size: 18px;
        padding: 12px;
        text-align: center;
        border: 2px solid;  /* Lighter border color */
        color: #4a6fa5;
        transition: 0.3s ease-in-out;
    }

    .stTextInput>div>div>input:focus {
        border-color: #7ea3d7 !important;
        box-shadow: 0px 0px 15px rgba(126, 163, 215, 0.3);
    }

    /* Select Box with updated colors */
    .stSelectbox>label {
        color: #4a6fa5 !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    /* Buttons with updated gradient */
    .stButton>button {
        background: linear-gradient(135deg, #7ea3d7, #a4c1e4);
        color: white;
        font-size: 22px;
        padding: 15px 25px;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        box-shadow: 2px 2px 10px rgba(126, 163, 215, 0.3);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #a4c1e4, #7ea3d7);
        transform: scale(1.05);
    }

    /* Messages with updated colors */
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
        background-color: rgba(142, 199, 171, 1) !important;
        color: white !important;
        box-shadow: 0px 0px 10px rgba(142, 199, 171, 0.8);
    }

    .stWarning {
        background-color: rgba(231, 129, 109, 1) !important;
        color: white !important;
        box-shadow: 0px 0px 10px rgba(231, 129, 109, 0.8);
    }
    </style>
"""
st.markdown(temp_css, unsafe_allow_html=True)


def overlay_name_on_template(name, event):
    templates = {
        "NSS Camp 2025": "templates/camp.jpg",  
        "Stem Cell Donation Drive": "templates/stemcell.jpg",  
        "Grain-a-thon 2.0": "templates/grainathon.jpg",   
        "Participation": "templates/various.jpg"
    }
    template_img = Image.open(templates.get(event, "templates/various.jpg"))  
    draw = ImageDraw.Draw(template_img)
    
    img_width, img_height = template_img.size
    x = img_width / 2
    y = img_height / 2 - 80 
    
    draw.text((x, y), name, fill=(0, 0, 0))
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

def is_name_in_csv(name):
    try:
        df = pd.read_csv("attendance/camp.csv")
        df["Name"] = df["Name"].str.strip().str.lower()
        return name.strip().lower() in df["Name"].values
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return False

def send_email(name, event, email, pdf_buffer):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Your Certificate for {event}"
        msg['From'] = "djsnss2025@gmail.com"
        msg['To'] = email
        msg.set_content(f"Dear {name},\n\nYour participation in {event} has been acknowledged. Your certificate is attached.")
        
        pdf_data = pdf_buffer.getvalue()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=f"{name}_{event}.pdf")
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("djsnss2025@gmail.com", "vqnu yshn ibhd eusx")
            server.send_message(msg)

    except Exception as e:
        st.error(f"Error sending email: {e}")

def main():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo, width=120)
    with col2:
        st.markdown('<div class="custom-title">DJS NSS Certificates</div>', unsafe_allow_html=True)
    
    user_input = st.text_input("Enter your full name:", key="name_input").strip().title()
    email_input = st.text_input("Enter your email:", key="email_input").strip()
    event = st.selectbox("Select Event", ["NSS Camp 2025", "Stem Cell Donation Drive", "Grain-a-thon 2.0", "Participation"])
    
    if st.button("Generate Certificate"):
        if user_input and email_input:
            if not is_name_in_csv(user_input):
                st.warning(f"⚠️ Name not found in the attendance list for {event}.")
                return
            img_with_overlay = overlay_name_on_template(user_input, event)
            st.image(img_with_overlay, caption="Generated Certificate", use_container_width=True)            
            pdf_buffer = generate_pdf_with_image(user_input, event)
            st.success("Certificate preview generated successfully!")
            st.download_button(
                label="Download Certificate PDF",
                data=pdf_buffer,
                file_name=f"{user_input}_{event}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            send_email(user_input, event, email_input, pdf_buffer)
            st.success("📨 You will receive the certificate on your email shortly. Please be patient.")
        else:
            st.warning("⚠️ Please enter a valid name and email.")

if __name__ == "__main__":
    main()

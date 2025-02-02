import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import base64

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
        font-size: 24px !important;
        font-weight: 500 !important;
    }
    .custom-image {
        border: 5px solid #0077b6;
        border-radius: 10px;
        padding: 5px;
        background-color: rgba(255, 255, 255, 0.1);
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
    .stError > div {
        background-color: rgba(255, 0, 0, 0.1) !important;
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
    @media only screen and (max-width: 640px) {
        .custom-image {
            display: none; 
        }
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv("WSAttendance.csv")
    data = data[(data["Day-1"] == True) | (data["Day-2"] == True)]
    return data

def overlay_name_on_template(template_img, name):
    img = template_img.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Allura-Regular.ttf", 175)
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_width, img_height = img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / (2.15)
    draw.text((x, y), name, fill=(0, 93, 143), font=font, stroke_width=2, stroke_fill=(0, 0, 255))
    return img

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def main():
    # Load data
    data = load_data()
    
    # Load templates
    template1 = Image.open("1Template.png")
    template2 = Image.open("2Template.png")
    template12 = Image.open("12Template.png")
    
    col1, col2 = st.columns([1, 4])
    with col2:
        st.markdown('<div class="custom-title">DJS NSS Event 2024 Certificate</div>', unsafe_allow_html=True)
    with col1:
        st.markdown(
            '<div class="custom-image"><img src="data:image/png;base64,{0}" width="125" /></div>'.format(
                image_to_base64(logo)
            ),
            unsafe_allow_html=True
        )
    
    st.markdown(
        '<div class="custom-text">This tool will verify your participation in the DJS NSS Event 2024 and automatically generate a personalized certificate with your name.<br> To get your certificate, please enter the name you used for registration in the field below and click "Enter". Once generated, you can download your certificate instantly.<br>Thank you for participating, and have a wonderful year ahead!</div>',
        unsafe_allow_html=True
    )
    
    user_input = st.text_input("What is your full name?").strip().title()
    st.markdown('<div class="custom-text">Please input your name in the above field. Thank you!</div>', unsafe_allow_html=True)
    
    if st.button("Enter Name"):
        with st.spinner("Loading...."):
            if user_input in data["Name"].str.title().values:
                selected_row = data[data["Name"].str.title() == user_input].iloc[0]
                name = selected_row["Name"].title()
                attendance_day1 = selected_row["Day-1"]
                attendance_day2 = selected_row["Day-2"]

                if attendance_day1 and attendance_day2:
                    img_with_overlay = overlay_name_on_template(template12, name)
                elif attendance_day1:
                    img_with_overlay = overlay_name_on_template(template1, name)
                elif attendance_day2:
                    img_with_overlay = overlay_name_on_template(template2, name)

                st.image(
                    img_with_overlay,
                    caption="Generated Certificate",
                    use_column_width=True,
                )
                
                download_buf = io.BytesIO()
                img_with_overlay.save(download_buf, format="PNG")
                if st.download_button(
                    "Download Certificate",
                    download_buf.getvalue(),
                    file_name=f"{selected_row['Name']}_DJS_NSS_Event.png",
                ):
                    st.success("Certificate downloaded!")
                st.toast("Certificate Successfully Generated 🥳🎉")
                st.balloons()

            elif user_input.strip() == "":
                st.warning("Name is a mandatory field", icon="⚠️")
            else:
                st.error("Sorry, name not found in the attendee database.")

if __name__ == "__main__":
    main()
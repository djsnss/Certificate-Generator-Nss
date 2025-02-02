import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Load logo image
logo = Image.open("NSS.png").resize((200, 200))
st.set_page_config(page_title="Synapse ML-Workshop", page_icon=logo)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    .stButton>button {
        background-color: black;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        font-size: 16px;
        padding: 10px;
    }
    .custom-image {
        border: 5px solid white;
        border-radius: 10px;
        padding: 5px;
        background-color: #333;
    }
    .custom-title {
        font-family: 'Allura';
        color: white;
        text-align: center;
        font-size: 36px;
        margin-top: 20px;
    }
    .custom-text {
        font-family: 'Allura';
        color: white;
        font-size: 18px;
        margin-top: 10px;
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


data = load_data()

template1 = Image.open("1Template.png")  ### First Day
template2 = Image.open("2Template.png")  ### Second Day
template12 = Image.open("12Template.png")  ### Both DAYS


# Function to OVERLAY name on template
def overlay_name_on_template(template_img, name):
    img = template_img.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Allura-Regular.ttf", 175)  # Adjust font and size
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    img_width, img_height = img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / (2.15)
    draw.text((x, y), name, fill=(0, 93, 143), font=font, stroke_width=2, stroke_fill=(0, 0, 255))  # Adjust text color
    return img

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def main():
    col1, col2 = st.columns([1, 4])
    with col2:
        st.markdown('<div class="custom-title">Synapse ML-Workshop 2024 Certificate</div>', unsafe_allow_html=True)
    with col1:
        st.markdown(
            '<div class="custom-image"><img src="data:image/png;base64,{0}" width="125" /></div>'.format(
                image_to_base64(logo)
            ),
            unsafe_allow_html=True
        )
    st.markdown(
        '<div class="custom-text">This tool will verify your participation in the Synapse ML-Workshop 2024 and automatically generate a personalized certificate with your name.<br> To get your certificate, please enter the name you used for registration in the field below and click "Enter". Once generated, you can download your certificate instantly.<br>Thank you for participating, and have a wonderful year ahead!</div>',
        unsafe_allow_html=True
    )
    user_input = st.text_input("What is your full name?").strip().title()
    st.write("Please input your name in the above field. Thank you!")
    if st.button("Enter Name"):
        with st.spinner("Loading...."):
            if user_input in data["Name"].str.title().values:
                selected_row = data[data["Name"].str.title() == user_input].iloc[0]
                name = selected_row["Name"].title()
                attendance_day1 = selected_row["Day-1"]  # Day 1 attendance Boolean
                attendance_day2 = selected_row["Day-2"]  # Day 2 attendance Boolean

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
                    file_name=f"{selected_row['Name']}_Synapse_WS24.png",
                ):
                    st.success("Certificate downloaded!")
                st.toast("Certificate Succesfully Generated 🥳🎉")
                st.balloons()

            elif user_input.strip() == "":
                st.warning("Name is a mandatory field")
            else:
                st.error("Sorry, name not found in the attendee database.")


if __name__ == "__main__":
    main()

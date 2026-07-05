import streamlit as st
from extract import extract_text
from parser import parse_text
from matcher import match_data

st.set_page_config(page_title="Citizenship Verification System", layout="centered")

st.title("🔹 Citizenship Verification System 🔹")
st.write("Upload citizenship image and enter details for verification")

# ---------------- USER INPUT ----------------
name = st.text_input("Name")
citizenship_no = st.text_input("Citizenship Number")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
birth_place = st.text_input("Birth Place")
permanent_address = st.text_area("Permanent Address")

uploaded_file = st.file_uploader("Upload Citizenship Image", type=["jpg", "jpeg", "png"])

# ---------------- BUTTON ----------------
if st.button("Verify"):

    if uploaded_file is not None:

        # Save uploaded image temporarily
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success("Image uploaded successfully!")

        # ---------------- OCR ----------------
        with st.spinner("Extracting text from image..."):
            text = extract_text(image_path)

        st.subheader("📄 Raw OCR Text")
        st.text(text)

        # ---------------- PARSE ----------------
        ocr_data = parse_text(text)

        st.subheader("🧠 Extracted Data")
        st.json(ocr_data)

        # ---------------- USER DATA ----------------
        user_data = {
            "name": name,
            "citizenship_no": citizenship_no,
            "dob": dob,
            "birth_place": birth_place,
            "permanent_address": permanent_address
        }

        # ---------------- MATCH ----------------
        result = match_data(user_data, ocr_data)

        st.subheader("🎯 Verification Result")

        if result["status"] == "VERIFIED":
            st.success(result)
        else:
            st.error(result)

    else:
        st.warning("Please upload an image first!")
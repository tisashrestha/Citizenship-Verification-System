import os, sys
if hasattr(os, "add_dll_directory"):
    torch_lib = os.path.join(sys.prefix, "Lib", "site-packages", "torch", "lib")
    if os.path.exists(torch_lib):
        os.add_dll_directory(torch_lib)

import streamlit as st
from validator import validate_front_side  
from extract import extract_text            
from parser import parse_text
from matcher import match_data

st.set_page_config(page_title="Advanced Citizenship Verification", layout="wide")

st.title("Advanced Citizenship Verification System")
st.write("Upload both sides of the citizenship card for full data & visual verification")

# side bar col
st.sidebar.header("User Details")
name = st.sidebar.text_input("Full Name")
citizenship_no = st.sidebar.text_input("Citizenship Number")
dob = st.sidebar.text_input("DOB (YYYY-MM-DD)")


# mid column 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("1.Back Side (OCR)")
    back_file = st.file_uploader("Upload Back Side", type=["jpg", "jpeg", "png"], key="back")
    if back_file:
        st.image(back_file, caption="Back Side Image", use_container_width=True)

with col2:
    st.subheader("2.Front Side (Verification)")
    front_file = st.file_uploader("Upload Front Side", type=["jpg", "jpeg", "png"], key="front")
    if front_file:
        st.image(front_file, caption="Front Side Image", use_container_width=True)




if st.button("Perform Full Verification"):
    if not (back_file and front_file):
        st.warning("Please upload both sides of the citizenship card.")
    elif not name or not citizenship_no:
        st.warning("Please enter all the required elements.")
    else:
        
        with open("temp_back.jpg", "wb") as f: f.write(back_file.read())
        with open("temp_front.jpg", "wb") as f: f.write(front_file.read())

        # verfication 1
        with st.spinner("Extracting data from the Back Side..."):
            raw_text = extract_text("temp_back.jpg")
            ocr_data = parse_text(raw_text)
            user_data = {
                "name": name,
                "citizenship_no": citizenship_no,
                "dob": dob
            }
            data_result = match_data(user_data, ocr_data)

        # verification 2
        with st.spinner("Validating the Front Side visual markers..."):
            is_visual_valid, visual_msg, detections, annotated_image = validate_front_side("temp_front.jpg")

        # final verification
        st.divider()
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.subheader("Data Match Results")
            if data_result["status"] == "VERIFIED":
                st.success(" Data Matched Successfully")
            else:
                st.error(f"{data_result['status']}")
            st.json(data_result)

        with res_col2:
            st.subheader("Visual Validation (YOLO)")
            if is_visual_valid:
                st.success(f"{visual_msg}")
            else:
                st.error(f"{visual_msg}")

            if annotated_image is not None:
                st.image(annotated_image, channels="BGR", caption="Detected Objects", use_container_width=True)

            for d in detections:
                st.write(f"- **{d['label']}**: {d['conf']:.2%}")

        st.divider()
        if data_result["status"] == "VERIFIED" and is_visual_valid:
            st.info("CITIZENSHIP IS FULLY VERIFIED & AUTHENTIC")
        else:
            st.error("VERIFICATION FAILED")
            if data_result["status"] != "VERIFIED":
                st.write("Data mismatch")
            if not is_visual_valid:
                st.write("Citizenship credentials Not detected")
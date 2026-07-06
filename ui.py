# --- DLL conflict fix: MUST be at the very top, before any other imports ---
import os, sys
if hasattr(os, "add_dll_directory"):
    torch_lib = os.path.join(sys.prefix, "Lib", "site-packages", "torch", "lib")
    if os.path.exists(torch_lib):
        os.add_dll_directory(torch_lib)

import streamlit as st
from validator import validate_front_side   # import torch-based module FIRST
from extract import extract_text            # then paddle-based modules
from parser import parse_text
from matcher import match_data

st.set_page_config(page_title="Advanced Citizenship Verification", layout="wide")

st.title("🔹 Advanced Citizenship Verification System")
st.write("Upload both sides of the citizenship card for full data & visual verification.")

# ---------------- SIDEBAR: USER INPUT ----------------
st.sidebar.header("User Details")
name = st.sidebar.text_input("Full Name")
citizenship_no = st.sidebar.text_input("Citizenship Number")
dob = st.sidebar.text_input("DOB (YYYY-MM-DD)")
birth_place = st.sidebar.text_input("Birth Place")
permanent_address = st.sidebar.text_area("Permanent Address")

# ---------------- MAIN AREA: FILE UPLOADS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Back Side (For OCR)")
    back_file = st.file_uploader("Upload Back Side", type=["jpg", "jpeg", "png"], key="back")
    if back_file:
        st.image(back_file, caption="Back Side Image", use_container_width=True)

with col2:
    st.subheader("2. Front Side (For Visual Validation)")
    front_file = st.file_uploader("Upload Front Side", type=["jpg", "jpeg", "png"], key="front")
    if front_file:
        st.image(front_file, caption="Front Side Image", use_container_width=True)

# ---------------- VERIFICATION LOGIC ----------------
if st.button("🚀 Perform Full Verification"):
    if not (back_file and front_file):
        st.warning("Please upload both sides of the citizenship card.")
    elif not name or not citizenship_no:
        st.warning("Please enter at least Name and Citizenship Number in the sidebar.")
    else:
        # Save temp files
        with open("temp_back.jpg", "wb") as f: f.write(back_file.read())
        with open("temp_front.jpg", "wb") as f: f.write(front_file.read())

        # PROCESS 1: OCR & Matching (Back Side)
        with st.spinner("Step 1: Extracting data from Back Side..."):
            raw_text = extract_text("temp_back.jpg")
            ocr_data = parse_text(raw_text)
            user_data = {
                "name": name, "citizenship_no": citizenship_no,
                "dob": dob, "birth_place": birth_place, "permanent_address": permanent_address
            }
            data_result = match_data(user_data, ocr_data)

        # PROCESS 2: YOLO Validation (Front Side)
        with st.spinner("Step 2: Validating Front Side visual markers..."):
            is_visual_valid, visual_msg, detections = validate_front_side("temp_front.jpg")

        # ---------------- FINAL REPORT ----------------
        st.divider()
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.subheader("📊 Data Match Results")
            if data_result["status"] == "VERIFIED":
                st.success("✅ Data Matched Successfully")
            else:
                st.error(f"❌ {data_result['status']}")
            st.json(data_result)

        with res_col2:
            st.subheader("👁️ Visual Validation (YOLO)")
            if is_visual_valid:
                st.success(f"✅ {visual_msg}")
            else:
                st.error(f"❌ {visual_msg}")

            for d in detections:
                st.write(f"- **{d['label']}**: {d['conf']:.2%}")

        st.divider()
        if data_result["status"] == "VERIFIED" and is_visual_valid:
            st.balloons()
            st.info("🎯 **FINAL VERDICT: CITIZENSHIP IS FULLY VERIFIED & AUTHENTIC**")
        else:
            st.error("⚠️ **FINAL VERDICT: VERIFICATION FAILED**")
            if data_result["status"] != "VERIFIED":
                st.write("- Reason: Data mismatch or OCR failure.")
            if not is_visual_valid:
                st.write("- Reason: Visual authenticity markers (Photo/Seal) not detected.")
from extract import extract_text
from parser import parse_text
from matcher import match_data

IMAGE_PATH = "images/citizenship.jpg"

def main():

    print("\n🔹 CITIZENSHIP VERIFICATION SYSTEM 🔹\n")

    # ---------------- USER INPUT ----------------
    user_data = {
        "name": input("Name: "),
        "citizenship_no": input("Citizenship No: "),
        "dob": input("DOB (YYYY-MM-DD): "),
        "birth_place": input("Birth Place: "),
        "permanent_address": input("Permanent Address: ")
    }

    # ---------------- OCR ----------------
    print("\n🔍 Processing image...")
    text = extract_text(IMAGE_PATH)

    print("\n--- RAW OCR TEXT ---\n", text)

    # ---------------- PARSE ----------------
    ocr_data = parse_text(text)

    print("\n--- OCR PARSED DATA ---\n", ocr_data)

    # ---------------- MATCH ----------------
    result = match_data(user_data, ocr_data)

    print("\n--- FINAL VERIFICATION RESULT ---\n", result)


if __name__ == "__main__":
    main()
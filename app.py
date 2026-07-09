from extract import extract_text
from parser import parse_text
from matcher import match_data

IMAGE_PATH = "images/citizenship.jpg"

def main():
    user_data = {
        "name": input("Name: "),
        "citizenship_no": input("Citizenship No: "),
        "dob": input("DOB (YYYY-MM-DD): ")
    }

    text = extract_text(IMAGE_PATH)
    ocr_data = parse_text(text)
    result = match_data(user_data, ocr_data)


if __name__ == "__main__":
    main()
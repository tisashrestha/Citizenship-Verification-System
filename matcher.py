from rapidfuzz import fuzz
import re

def get_digits(text):
    if not text: return ""
    return "".join(filter(str.isdigit, str(text)))

def match_data(user, ocr):
    u_name = str(user.get("name") or "").strip().upper()
    o_name = str(ocr.get("name") or "").strip().upper()
    
    u_cid = get_digits(user.get("citizenship_no"))
    o_cid = get_digits(ocr.get("citizenship_no"))

    name_score = fuzz.token_sort_ratio(u_name, o_name)
    cid_digits_score = fuzz.ratio(u_cid, o_cid)
    cid_match = (u_cid == o_cid) or (cid_digits_score > 90 and len(u_cid) > 5)


    u_dob = str(user.get("dob") or "").strip()
    o_dob = str(ocr.get("dob") or "").strip()
    dob_match = (u_dob == o_dob)


    result = {
        "name_score": round(name_score, 2),
        "citizenship_match": bool(cid_match),
        "dob_match": bool(dob_match),
    }

    
    if cid_match and name_score >= 80:
        if dob_match:
            result["status"] = "VERIFIED"
        else:
            result["status"] = "NOT VERIFIED (Details Mismatch)"
    else:
        result["status"] = "NOT VERIFIED (Identity Mismatch)"

    return result
from rapidfuzz import fuzz
import re

def get_digits(text):
    """Extracts only numeric digits from a string."""
    if not text: return ""
    return "".join(filter(str.isdigit, str(text)))

def match_data(user, ocr):
    # 1. Clean Inputs
    u_name = str(user.get("name") or "").strip().upper()
    o_name = str(ocr.get("name") or "").strip().upper()
    
    u_cid = get_digits(user.get("citizenship_no"))
    o_cid = get_digits(ocr.get("citizenship_no"))

    # 2. Name Match (Fuzzy)
    name_score = fuzz.token_sort_ratio(u_name, o_name)

    # 3. CID Match (Digit-only comparison)
    # If the digits are identical, match is True.
    # If they are 95% similar (e.g., OCR missed one digit), match is also True.
    cid_digits_score = fuzz.ratio(u_cid, o_cid)
    cid_match = (u_cid == o_cid) or (cid_digits_score > 90 and len(u_cid) > 5)

    # 4. DOB Match
    # Normalize dates to string comparison
    u_dob = str(user.get("dob") or "").strip()
    o_dob = str(ocr.get("dob") or "").strip()
    dob_match = (u_dob == o_dob)

    # 5. Address Match (The Pool Strategy)
    # Combine everything extracted into one pool to check against user input
    # ocr_pool = f"{ocr.get('birth_place') or ''} {ocr.get('permanent_address') or ''}".upper()
    
    # u_birth = str(user.get("birth_place") or "").upper()
    # u_perm = str(user.get("permanent_address") or "").upper()
    
    # birth_score = fuzz.token_set_ratio(u_birth, ocr_pool)
    # addr_score = fuzz.token_set_ratio(u_perm, ocr_pool)

    # 6. Final Result Object
    result = {
        "name_score": round(name_score, 2),
        "citizenship_match": bool(cid_match),
        "dob_match": bool(dob_match),
        # "birth_place_score": round(birth_score, 2),
        # "address_score": round(addr_score, 2)
    }

    # ---------------- VERIFICATION LOGIC ----------------
    # High confidence criteria:
    # - CID must match (digit similarity > 90%)
    # - Name must be very close (80%+)
    # - One other piece of evidence (DOB match OR Address found in pool)
    
    if cid_match and name_score >= 80:
        if dob_match:
            result["status"] = "VERIFIED"
        else:
            result["status"] = "NOT VERIFIED (Details Mismatch)"
    else:
        result["status"] = "NOT VERIFIED (Identity Mismatch)"

    return result
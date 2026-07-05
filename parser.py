import re

def clean(text):
    if not text: return ""
    # Keep alphanumeric and specific separators (including / and -)
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z0-9\s:/.-]', ' ', text)).strip()

def extract_dob(text):
    months_map = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    
    # 1. Mask "Act 2006"
    clean_text = re.sub(r'Act\s*,?\s*2006', 'LEGAL_TEXT', text, flags=re.I)
    
    # 2. Resilient Year Search
    year_match = re.search(r'Y[ea4]{1,2}r?\s*[:.\-]?\s*(19\d{2}|20\d{2})', clean_text, re.I)
    year = year_match.group(1) if year_match else None
    
    # 3. Resilient Day Search
    day_match = re.search(r'D[ay4]{1,2}y?\s*[:.\-]?\s*(\d{1,2})', text, re.I)
    day = day_match.group(1).zfill(2) if day_match else None
    
    # 4. Resilient Month Search
    month = None
    month_label_match = re.search(r'M[o0a]{1,2}[nt]{1,2}h?\s*[:.\-]?\s*([A-Z0-9]+)', text, re.I)
    
    if month_label_match:
        m_val = month_label_match.group(1).upper()
        if m_val.isdigit():
            month = m_val.zfill(2)
        else:
            month = months_map.get(m_val[:3])
            
    if not month:
        for name, num in months_map.items():
            if name in text.upper():
                month = num
                break

    if year and month and day:
        return f"{year}-{month}-{day}"
    return None

def parse_text(text):
    lines = [clean(l) for l in text.split('\n') if len(l.strip()) > 2]
    flat_text = " ".join(lines)

    data = {
        "name": None, 
        "citizenship_no": None, 
        "dob": extract_dob(text),
        "birth_place": None, 
        "permanent_address": None
    }

    # ---------------- 1. Citizenship No (UPDATED) ----------------
    # Updated regex: 
    # Starts with digits, followed by a separator (-, /, ., or space) 
    # Supports 2 to 5 segments (e.g., 2178/255 or 27-01-72-18351)
    cid = re.search(r'(\d+[\-/.\s]\d+(?:[\-/.\s]\d+){0,4})', flat_text)
    if cid:
        # Standardize: Convert spaces and dots to dashes, but keep slashes '/' and dashes '-'
        raw_cid = cid.group(1).replace(' ', '-').replace('.', '-')
        # Strip trailing noise but ALLOW both digits and slashes to remain at the end
        data["citizenship_no"] = re.sub(r'[^0-9/]$', '', raw_cid).strip()

    # ---------------- 2. Name ----------------
    blacklist = ["NEPAL", "CITIZENSHIP", "CERTIFICATE", "WARD", "DISTRICT", "METROPOLITAN", "MALE", "FEMALE", "PROVINCE", "FULLNAME"]
    for line in lines:
        if line.isupper() and 2 <= len(line.split()) <= 5:
            clean_name = re.sub(r'(FULLNAME|FULL NAME|NAME|[:.])', '', line, flags=re.I).strip()
            if not any(x in clean_name.upper() for x in blacklist) and len(clean_name) > 3:
                data["name"] = clean_name
                break

    # ---------------- 3. Addresses ----------------
    addr_keys = ["WARD", "DISTRICT", "DINTRICT", "METROPOLITAN", "MUNICIPALITY", "PROVINCE", "LALITPUR", "KATHMANDU", "DHARAN"]
    addr_lines = [l for l in lines if any(k in l.upper() for k in addr_keys)]
    
    birth_idx = re.search(r'B[irn]{2,3}th?\s*P[l1]ace', flat_text, re.I)
    perm_idx = re.search(r'Perm[an]{2,4}ent', flat_text, re.I)
    
    if addr_lines:
        b_pos = birth_idx.start() if birth_idx else 0
        p_pos = perm_idx.start() if perm_idx else 9999
        
        mid = len(addr_lines) // 2
        if b_pos < p_pos:
            data["birth_place"] = " ".join(addr_lines[:mid])
            data["permanent_address"] = " ".join(addr_lines[mid:])
        else:
            data["permanent_address"] = " ".join(addr_lines[:mid])
            data["birth_place"] = " ".join(addr_lines[mid:])

    return data
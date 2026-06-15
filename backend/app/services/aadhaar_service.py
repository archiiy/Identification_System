import re
from app.logger.elastic_logger import push_log


def validate_verhoeff(number):
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    ]

    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
    ]

    c = 0

    for i, item in enumerate(reversed(number)):
        c = d[c][p[i % 8][int(item)]]

    return c == 0


def extract_aadhaar(text):
    matches = re.findall(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text)

    if not matches:
        
        push_log({
            "event": "aadhaar_verification",
            "aadhaar": None,
            "verification": "failed",
            "reason": "Number not found"
        })
        
        return {
            "aadhaar": None,
            "valid": False,
            "reason": "Number not found",
        }

    aadhaar = matches[0]
    checksum = validate_verhoeff(aadhaar)

    result = {
        "aadhaar": f"{aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}",
        "valid": checksum,
        "reason": "Checksum Passed" if checksum else "Checksum Failed",
    }

    push_log({
        "event": "aadhaar_verification",
        "aadhaar": result["aadhaar"],
        "verification": "passed" if result["valid"] else "failed",
        "reason": result["reason"],
    })

    return result
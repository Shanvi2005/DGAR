import re
from datetime import datetime

REQUIRED_KEYS = {
    "subject", "subject_type",
    "relationship",
    "object", "object_type",
    "timestamp"
}

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def is_valid_timestamp(date_str: str) -> bool:
    if not DATE_PATTERN.match(date_str):
        return False
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt > datetime.now():
            return False
        if dt.year < 1900:
            return False
        return True
    except ValueError:
        return False


def validate_triplet(triplet: dict) -> bool:
    # 1️⃣ Check required keys
    if not REQUIRED_KEYS.issubset(triplet.keys()):
        return False
    
    # 2️⃣ Check all values are non-empty strings
    for key in REQUIRED_KEYS:
        if not isinstance(triplet[key], str):
            return False
        if not triplet[key].strip():
            return False

    # 3️⃣ Timestamp validation
    if not is_valid_timestamp(triplet["timestamp"]):
        return False

    return True

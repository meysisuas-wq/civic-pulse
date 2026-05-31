import re
from typing import List

def validate_email(email: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validate_citizen_id(cid: str) -> bool:
    return bool(re.match(r'^\d{16}$', cid))

def validate_password_strength(password: str) -> List[str]:
    errors = []
    if len(password) < 8: errors.append("Min 8 characters")
    if not re.search(r'[A-Z]', password): errors.append("Need uppercase")
    if not re.search(r'[a-z]', password): errors.append("Need lowercase")
    if not re.search(r'\d', password): errors.append("Need digit")
    return errors

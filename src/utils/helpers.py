import re, secrets, hashlib
from datetime import datetime, timezone

def generate_request_number(prefix: str = "CP") -> str:
    now = datetime.now(timezone.utc)
    return f"{prefix}-{now.strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"

def sanitize_input(text: str) -> str:
    if not text: return ""
    return re.sub(r'<[^>]+>', '', text).strip()

def mask_citizen_id(cid: str) -> str:
    if len(cid) <= 4: return cid
    return '*' * (len(cid) - 4) + cid[-4:]

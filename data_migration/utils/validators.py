import re
from datetime import datetime

# --- Email Validation ---
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# --- Phone Number Validation ---
def is_valid_phone(phone):
    pattern = r'^(\+1\s?)?(\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}$'
    if phone is None or phone.strip() == "":
        return True  # allow null
    return re.match(pattern, phone)

# --- Date Validation and Conversion ---
def is_valid_date(date_str, format="%m/%d/%Y"):
    if not date_str or date_str.strip() == "":
        return ""  # treat empty string as NULL-compatible
    try:
        parsed_date = datetime.strptime(date_str.strip(), format)
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return False

# --- Date Order Validation ---
def is_date_order_valid(start, end):
    if not start or not end:
        return True
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        return end_dt >= start_dt
    except ValueError:
        return False

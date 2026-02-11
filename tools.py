import re

# Curated lists for demo purposes
SCAM_NUMBERS = ["1234567890", "9999999999", "0000000000"]
SUSPICIOUS_DOMAINS = ["scam-bank.com", "gift-card-win.tk", "verify-aadhaar.xyz"]

BANK_DIRECTORY = {
    "SBI": {"Block SMS": "BLOCK MS <Last 4 digits> to 567676", "Call": "1800 1234", "USSD": "*595#"},
    "HDFC": {"Block SMS": "BLOCK to 5676708", "Call": "1800 202 6161", "USSD": "*711#"},
    "ICICI": {"Block SMS": "BLOCK <Last 4 digits> to 5676766", "Call": "1800 1080", "USSD": "*525#"},
    "Axis": {"Block SMS": "BLOCKCARD to 56161600", "Call": "1800 419 5959", "USSD": "*99*45#"},
    "PNB": {"Block SMS": "SBLOCK <Account No> to 5607040", "Call": "1800 1800", "USSD": "*99*22#"}
}

def check_scam(input_text):
    """Checks if a number or URL matches known scam patterns."""
    input_text = input_text.strip().lower()
    
    # Check numbers
    if re.match(r'^\+?\d{10,12}$', input_text.replace(" ", "")):
        clean_num = "".join(filter(str.isdigit, input_text))
        if clean_num in SCAM_NUMBERS:
            return "⚠️ This number is found in our SCAM database. DO NOT engage."
        return "✅ This number is not in our known scam database. (Always stay cautious!)"
    
    # Check URLs
    for domain in SUSPICIOUS_DOMAINS:
        if domain in input_text:
            return "🚨 DANGER: This domain is a known phishing/scam site. CLOSE IT NOW."
    
    if "http" in input_text or "." in input_text:
        return "ℹ️ URL not in our blocklist, but verify if the SSL (padlock) exists and looks official."

    return "❌ Input doesn't look like a phone number or URL."

def get_bank_info(bank_name):
    return BANK_DIRECTORY.get(bank_name.upper())

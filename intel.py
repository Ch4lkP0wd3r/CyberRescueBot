import logging
import re

logger = logging.getLogger(__name__)

# Basic keywords for intent mapping
INTENT_MAP = {
    'menu_lost': [r'money', r'lost', r'stole', r'fraud', r'bank', r'transaction', r'paisa', r'loot'],
    'menu_hacked': [r'hack', r'access', r'login', r'password', r'instagram', r'email', r'facebook', r'otp'],
    'menu_fir': [r'fir', r'police', r'complain', r'report', r'portal', r'case'],
    'menu_safe': [r'tips', r'safe', r'protect', r'advice', r'how to']
}

def detect_intent(text: str):
    """Detects user intent based on keyword matching."""
    text = text.lower()
    
    # Check for direct matches or keywords
    for intent, patterns in INTENT_MAP.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent
                
    return None

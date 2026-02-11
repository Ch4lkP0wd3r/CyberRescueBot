from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

# Language Selection Keyboard
LANG_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
        InlineKeyboardButton("हिन्दी 🇮🇳", callback_data="lang_hi")
    ]
])

# Main Menu Inline Keyboard
def get_main_menu(lang='en'):
    if lang == 'hi':
        keyboard = [
            [InlineKeyboardButton("FIR दर्ज करें 📝", callback_data="menu_fir"),
             InlineKeyboardButton("पैसे खो गए 💸", callback_data="menu_lost")],
            [InlineKeyboardButton("अकाउंट हैक 🔐", callback_data="menu_hacked"),
             InlineKeyboardButton("सुरक्षित रहें 🛡️", callback_data="menu_safe")],
            [InlineKeyboardButton("रिपोर्ट दर्ज करें 📑", callback_data="menu_report"),
             InlineKeyboardButton("एक्शन सेंटर ⚡", callback_data="menu_action")],
            [InlineKeyboardButton("भाषा बदलें 🌐", callback_data="menu_lang"),
             InlineKeyboardButton("चैट समाप्त करें ❌", callback_data="menu_end")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("File FIR 📝", callback_data="menu_fir"),
             InlineKeyboardButton("Lost Money 💸", callback_data="menu_lost")],
            [InlineKeyboardButton("Account Hacked 🔐", callback_data="menu_hacked"),
             InlineKeyboardButton("Stay Safe 🛡️", callback_data="menu_safe")],
            [InlineKeyboardButton("Generate Report 📑", callback_data="menu_report"),
             InlineKeyboardButton("Action Center ⚡", callback_data="menu_action")],
            [InlineKeyboardButton("Change Language 🌐", callback_data="menu_lang"),
             InlineKeyboardButton("End Chat ❌", callback_data="menu_end")]
        ]
    return InlineKeyboardMarkup(keyboard)

# Content Dictionary
STRINGS = {
    'en': {
        'start': "👋 *Welcome to CyberRescue v2!*\n\nI am your advanced AI assistant for cybercrime recovery. Select an option below to begin.",
        'help': "🆘 *Help Menu*\n\n• *File FIR*: Official steps.\n• *Lost Money*: Financial emergency.\n• *Report*: Generate a professional PDF report.\n• *Safe*: Tips.",
        'fir': "📝 *File a Complaint*\n\n1️⃣ Portal: https://cybercrime.gov.in\n2️⃣ Helpline: 1930\n\nClick the button below to open the portal directly.",
        'lost': "💸 *Financial Emergency*\n\n🔴 *Call 1930 IMMEDIATELY*.\n1️⃣ Freeze bank accounts.\n2️⃣ Save transaction IDs.",
        'hacked': "🔐 *Account Recovery*\n\n1️⃣ Change Passwords.\n2️⃣ Enable 2FA.\n3️⃣ Logout other devices.",
        'safe': "🛡️ *Safety Tips*\n\n• Never share OTP.\n• Use strong passwords.\n• Don't click unknown links.",
        'report_start': "📝 *Report Assistant*\nLet's generate your official PDF report.",
        'btn_portal': "Open Cybercrime Portal 🌐",
        'end_chat': "👋 *Goodbye!*\n\nYou have ended the chat session. Stay safe online! Type /start whenever you need help again.",
        'cancel_btn': "Cancel ❌",
        'subscribed': "🔔 *Subscribed!* You will now receive daily digital safety tips.",
        'unsubscribed': "🔕 *Unsubscribed!* You will no longer receive daily tips.",
        'stats': "📊 *CyberRescue Stats*\n\n👥 Users: {users}\n📑 Reports: {reports}\n🔔 Subscribers: {subs}",
        'history': "📜 *Your Report History*\n\n",
        'no_history': "You haven't filed any reports yet.",
        'action_center': "⚡ *Action Center*\nChoose a tool to take direct action against cybercrime.",
        'scamcheck_prompt': "🔍 *Scam Check*\nSend a phone number or website link to check if it's a known scam.",
        'checklist_header': "✅ *Recovery Checklist*\nClick an item to toggle its status.",
        'bank_dir_header': "🏛️ *Bank Emergency Directory*\nSelect a bank to see blocking details.",
        'btn_scam': "Check Scam 🔍",
        'btn_checklist': "My Checklist ✅",
        'btn_bank_dir': "Bank Directory 🏛️",
        'btn_drafter': "Draft Complaint ✍️"
    },
    'hi': {
        'start': "👋 *CyberRescue v2 में आपका स्वागत है!*\n\nमैं साइबर अपराध से उबरने में आपकी मदद करने वाला उन्नत AI सहायक हूँ। शुरू करने के लिए नीचे एक विकल्प चुनें।",
        'help': "🆘 *सहायता मेनू*\n\n• *FIR दर्ज करें*: आधिकारिक कदम।\n• *पैसे खो गए*: वित्तीय आपातकाल।\n• *रिपोर्ट*: पीडीएफ रिपोर्ट बनाएं।\n• *सुरक्षित*: टिप्स।",
        'fir': "📝 *शिकायत दर्ज करें*\n\n1️⃣ पोर्टल: https://cybercrime.gov.in\n2️⃣ हेल्पलाइन: 1930\n\nपोर्टल खोलने के लिए नीचे दिए गए बटन पर क्लिक करें।",
        'lost': "💸 *वित्तीय आपातकाल*\n\n🔴 *तुरंत 1930 पर कॉल करें*।\n1️⃣ बैंक खाते फ्रीज करें।\n2️⃣ ट्रांजेक्शन आईडी सुरक्षित रखें।",
        'hacked': "🔐 *अकाउंट रिकवरी*\n\n1️⃣ पासवर्ड बदलें।\n2️⃣ 2FA सक्षम करें।\n3️⃣ अन्य डिवाइस लॉगआउट करें।",
        'safe': "🛡️ *सुरक्षा टिप्स*\n\n• कभी भी OTP साझा न करें।\n• मजबूत पासवर्ड का प्रयोग करें।\n• अज्ञात लिंक पर क्लिक न करें।",
        'report_start': "📝 *रिपोर्ट सहायक*\nआइए आपकी आधिकारिक पीडीएफ रिपोर्ट बनाएं।",
        'btn_portal': "साइबर पोर्टल खोलें 🌐",
        'end_chat': "👋 *अलविदा!*\n\nआपने चैट सत्र समाप्त कर दिया है। ऑनलाइन सुरक्षित रहें! जब भी आपको फिर से सहायता की आवश्यकता हो, /start टाइप करें।",
        'cancel_btn': "रद्द करें ❌",
        'subscribed': "🔔 *सदस्यता ली गई!* अब आप दैनिक सुरक्षा टिप्स प्राप्त करेंगे।",
        'unsubscribed': "🔕 *सदस्यता समाप्त!* अब आपको दैनिक टिप्स नहीं मिलेंगे।",
        'stats': "📊 *साइबर रेस्क्यू आंकड़े*\n\n👥 उपयोगकर्ता: {users}\n📑 रिपोर्ट: {reports}\n🔔 ग्राहक: {subs}",
        'history': "📜 *आपका रिपोर्ट इतिहास*\n\n",
        'no_history': "आपने अभी तक कोई रिपोर्ट दर्ज नहीं की है।",
        'action_center': "⚡ *एक्शन सेंटर*\nसाइबर अपराध के खिलाफ सीधे कार्रवाई करने के लिए एक उपकरण चुनें।",
        'scamcheck_prompt': "🔍 *स्कैम चेक*\nकोई फोन नंबर या वेबसाइट लिंक भेजें यह जांचने के लिए कि क्या यह कोई जाना-माना स्कैम है।",
        'checklist_header': "✅ *रिकवरी चेकलिस्ट*\nकिसी आइटम पर क्लिक करके उसका स्टेटस बदलें।",
        'bank_dir_header': "🏛️ *बैंक इमरजेंसी डायरेक्टरी*\nब्लॉक करने का विवरण देखने के लिए एक बैंक चुनें।",
        'btn_scam': "स्कैम चेक 🔍",
        'btn_checklist': "मेरी चेकलिस्ट ✅",
        'btn_bank_dir': "बैंक डायरेक्टरी 🏛️",
        'btn_drafter': "शिकायत ड्राफ्ट करें ✍️"
    }
}

# Image Paths
POSTERS = {
    'passwords': '/home/ch4lkp0wd3r/.gemini/antigravity/brain/79901016-ade4-4239-bb27-7e18b21aee61/safety_poster_passwords_png_1770800364900.png',
    'phishing': '/home/ch4lkp0wd3r/.gemini/antigravity/brain/79901016-ade4-4239-bb27-7e18b21aee61/safety_poster_phishing_png_1770800385686.png',
    'otp': '/home/ch4lkp0wd3r/.gemini/antigravity/brain/79901016-ade4-4239-bb27-7e18b21aee61/safety_poster_otp_png_1770800413445.png'
}

# Reporting Flow Keyboards
INCIDENT_TYPES_KB = {
    'en': InlineKeyboardMarkup([
        [InlineKeyboardButton("Financial Fraud 💸", callback_data="rep_type_Financial")],
        [InlineKeyboardButton("Account Compromise 🔐", callback_data="rep_type_Account")],
        [InlineKeyboardButton("Identity Theft 👤", callback_data="rep_type_Identity")],
        [InlineKeyboardButton("Other/General 📝", callback_data="rep_type_Other")]
    ]),
    'hi': InlineKeyboardMarkup([
        [InlineKeyboardButton("वित्तीय धोखाधड़ी 💸", callback_data="rep_type_Financial")],
        [InlineKeyboardButton("अकाउंट के साथ छेड़छाड़ 🔐", callback_data="rep_type_Account")],
        [InlineKeyboardButton("पहचान की चोरी 👤", callback_data="rep_type_Identity")],
        [InlineKeyboardButton("अन्य 📝", callback_data="rep_type_Other")]
    ])
}

PLATFORMS_KB = {
    'en': InlineKeyboardMarkup([
        [InlineKeyboardButton("SBI / Bank", callback_data="rep_plat_SBI"), InlineKeyboardButton("HDFC / Bank", callback_data="rep_plat_HDFC")],
        [InlineKeyboardButton("Instagram", callback_data="rep_plat_Instagram"), InlineKeyboardButton("Facebook", callback_data="rep_plat_Facebook")],
        [InlineKeyboardButton("WhatsApp", callback_data="rep_plat_WhatsApp"), InlineKeyboardButton("OLX / Quickr", callback_data="rep_plat_OLX")],
        [InlineKeyboardButton("Other", callback_data="rep_plat_Other")]
    ]),
    'hi': InlineKeyboardMarkup([
        [InlineKeyboardButton("एसबीआई / बैंक", callback_data="rep_plat_SBI"), InlineKeyboardButton("एचडीएफसी / बैंक", callback_data="rep_plat_HDFC")],
        [InlineKeyboardButton("इंस्टाग्राम", callback_data="rep_plat_Instagram"), InlineKeyboardButton("फेसबुक", callback_data="rep_plat_Facebook")],
        [InlineKeyboardButton("व्हाट्सएप", callback_data="rep_plat_WhatsApp"), InlineKeyboardButton("ओएलएक्स", callback_data="rep_plat_OLX")],
        [InlineKeyboardButton("अन्य", callback_data="rep_plat_Other")]
    ])
}

DATES_KB = {
    'en': InlineKeyboardMarkup([
        [InlineKeyboardButton("Today", callback_data="rep_date_Today"), InlineKeyboardButton("Yesterday", callback_data="rep_date_Yesterday")],
        [InlineKeyboardButton("Last Week", callback_data="rep_date_LastWeek"), InlineKeyboardButton("Custom", callback_data="rep_date_Custom")]
    ]),
    'hi': InlineKeyboardMarkup([
        [InlineKeyboardButton("आज", callback_data="rep_date_Today"), InlineKeyboardButton("कल", callback_data="rep_date_Yesterday")],
        [InlineKeyboardButton("पिछले हफ्ते", callback_data="rep_date_LastWeek"), InlineKeyboardButton("कस्टम", callback_data="rep_date_Custom")]
    ])
}

TWO_FA_KB = {
    'en': InlineKeyboardMarkup([
        [InlineKeyboardButton("Enabled ✅", callback_data="rep_2fa_Enabled"), InlineKeyboardButton("Disabled ❌", callback_data="rep_2fa_Disabled")],
        [InlineKeyboardButton("I don't know ❓", callback_data="rep_2fa_Unknown")]
    ]),
    'hi': InlineKeyboardMarkup([
        [InlineKeyboardButton("सक्षम (Enabled) ✅", callback_data="rep_2fa_Enabled"), InlineKeyboardButton("अक्षम (Disabled) ❌", callback_data="rep_2fa_Disabled")],
        [InlineKeyboardButton("मुझे नहीं पता ❓", callback_data="rep_2fa_Unknown")]
    ])
}

RECOVERY_KB = {
    'en': InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes, I have access ✅", callback_data="rep_rec_Yes"), InlineKeyboardButton("No, hacker changed it ❌", callback_data="rep_rec_No")],
        [InlineKeyboardButton("Not sure ⚖️", callback_data="rep_rec_Maybe")]
    ]),
    'hi': InlineKeyboardMarkup([
        [InlineKeyboardButton("हाँ, मेरे पास एक्सेस है ✅", callback_data="rep_rec_Yes"), InlineKeyboardButton("नहीं, हैकर ने बदल दिया ❌", callback_data="rep_rec_No")],
        [InlineKeyboardButton("पक्का नहीं ⚖️", callback_data="rep_rec_Maybe")]
    ])
}

PORTAL_URL = "https://cybercrime.gov.in"

# Button for Portal
def get_portal_button(lang='en'):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(STRINGS[lang]['btn_portal'], web_app=WebAppInfo(url=PORTAL_URL))
    ]])

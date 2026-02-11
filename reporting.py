import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import database
import pdf_generator
import drafter
import constants
from constants import STRINGS

logger = logging.getLogger(__name__)

# State constants
INCIDENT_TYPE, PLATFORM, DATE_OCCURRED, FINANCIAL_AMOUNT, FINANCIAL_TXID, ACCOUNT_2FA, ACCOUNT_REC, EXTRA_DETAILS = range(8)

# specialized questions
FORENSIC_QS = {
    'en': {
        'type': "What happened? (Select a category)",
        'plat': "Where did this happen? (Select Platform/Bank)",
        'date': "When did this happen?",
        'fin_amt': "How much money was lost? (Enter amount in INR)",
        'fin_txid': "Do you have the Transaction ID? (Type it or 'No')",
        'acc_2fa': "Was Two-Factor Authentication (2FA) enabled?",
        'acc_rec': "Do you still have access to the recovery email/phone?",
        'id_susp': "Do you know the suspect? (Provide Username/Phone or 'Unknown')",
        'id_doc': "What information was compromised? (e.g. Pan Card, Photos)",
        'extra': "Describe the incident or any other details:"
    },
    'hi': {
        'type': "क्या हुआ था? (एक श्रेणी चुनें)",
        'plat': "यह कहाँ हुआ? (प्लेटफॉर्म/बैंक चुनें)",
        'date': "यह कब हुआ?",
        'fin_amt': "कितने पैसे खो गए? (राशि दर्ज करें)",
        'fin_txid': "क्या आपके पास ट्रांजेक्शन आईडी है? (दर्ज करें या 'नहीं' लिखें)",
        'acc_2fa': "क्या टू-फैक्टर ऑथेंटिकेशन (2FA) सक्षम था?",
        'acc_rec': "क्या आपके पास अभी भी रिकवरी ईमेल/फोन का उपयोग है?",
        'id_susp': "क्या आप संदिग्ध को जानते हैं? (यूजरनेम/फोन या 'अज्ञात' लिखें)",
        'id_doc': "क्या जानकारी लीक हुई? (जैसे पैन कार्ड, तस्वीरें)",
        'extra': "घटना का विवरण या कोई अन्य जानकारी दें:"
    }
}

# Add new states
INCIDENT_TYPE, PLATFORM, DATE_OCCURRED, FINANCIAL_AMOUNT, FINANCIAL_TXID, ACCOUNT_2FA, ACCOUNT_REC, IDENTITY_SUSPECT, IDENTITY_DOCS, EXTRA_DETAILS = range(10)

async def get_incident_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = database.get_user_language(update.effective_user.id)
    incident_type = query.data.split("_")[2]
    context.user_data['incident_type'] = incident_type
    
    await query.edit_message_text(f"*Step 2:* {FORENSIC_QS[lang]['plat']}", reply_markup=constants.PLATFORMS_KB[lang], parse_mode='Markdown')
    return PLATFORM

async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = database.get_user_language(update.effective_user.id)
    platform = query.data.split("_")[2]
    context.user_data['platform'] = platform
    context.user_data['metadata']['Platform/Bank'] = platform
    
    # Branching Logic
    inc_type = context.user_data['incident_type']
    if inc_type == "Financial":
        await query.edit_message_text(f"💰 {FORENSIC_QS[lang]['fin_amt']}", parse_mode='Markdown')
        return FINANCIAL_AMOUNT
    elif inc_type == "Account":
        await query.edit_message_text(f"🔐 {FORENSIC_QS[lang]['acc_2fa']}", reply_markup=constants.TWO_FA_KB[lang], parse_mode='Markdown')
        return ACCOUNT_2FA
    elif inc_type == "Identity":
        await query.edit_message_text(f"👤 {FORENSIC_QS[lang]['id_susp']}", parse_mode='Markdown')
        return IDENTITY_SUSPECT
    else:
        await query.edit_message_text(f"📅 {FORENSIC_QS[lang]['date']}", reply_markup=constants.DATES_KB[lang], parse_mode='Markdown')
        return DATE_OCCURRED

# ... (Previous code remains unchanged) ...

# Identity Branch
async def get_id_suspect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = database.get_user_language(update.effective_user.id)
    context.user_data['metadata']['Suspect Details'] = update.message.text
    await update.message.reply_text(f"📄 {FORENSIC_QS[lang]['id_doc']}", parse_mode='Markdown')
    return IDENTITY_DOCS

async def get_id_docs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = database.get_user_language(update.effective_user.id)
    context.user_data['metadata']['Compromised Info'] = update.message.text
    await update.message.reply_text(f"📅 {FORENSIC_QS[lang]['date']}", reply_markup=constants.DATES_KB[lang], parse_mode='Markdown')
    return DATE_OCCURRED

# Financial Branch
async def get_fin_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = database.get_user_language(update.effective_user.id)
    context.user_data['metadata']['Amount Lost'] = update.message.text
    await update.message.reply_text(f"📑 {FORENSIC_QS[lang]['fin_txid']}", parse_mode='Markdown')
    return FINANCIAL_TXID

async def get_fin_txid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = database.get_user_language(update.effective_user.id)
    context.user_data['metadata']['Transaction ID'] = update.message.text
    await update.message.reply_text(f"📅 {FORENSIC_QS[lang]['date']}", reply_markup=constants.DATES_KB[lang], parse_mode='Markdown')
    return DATE_OCCURRED

# Account Branch
async def get_acc_2fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = database.get_user_language(update.effective_user.id)
    val = query.data.split("_")[2]
    context.user_data['metadata']['2FA Status'] = val
    await query.edit_message_text(f"📧 {FORENSIC_QS[lang]['acc_rec']}", reply_markup=constants.RECOVERY_KB[lang], parse_mode='Markdown')
    return ACCOUNT_REC

async def get_acc_rec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    lang = database.get_user_language(update.effective_user.id)
    val = query.data.split("_")[2]
    context.user_data['metadata']['Recovery Access'] = val
    await query.edit_message_text(f"📅 {FORENSIC_QS[lang]['date']}", reply_markup=constants.DATES_KB[lang], parse_mode='Markdown')
    return DATE_OCCURRED

# Common Final Steps
async def get_date_occurred(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    lang = database.get_user_language(update.effective_user.id)
    if query:
        await query.answer()
        date_val = query.data.split("_")[2]
        if date_val == "Custom":
            await query.edit_message_text("Please type the date and time manually:")
            return DATE_OCCURRED
        context.user_data['incident_date'] = date_val
    else:
        context.user_data['incident_date'] = update.message.text

    msg = update.callback_query.message if update.callback_query else update.message
    await msg.reply_text(f"✍️ {FORENSIC_QS[lang]['extra']}", parse_mode='Markdown')
    return EXTRA_DETAILS

async def get_extra_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    lang = database.get_user_language(user.id)
    details = update.message.text
    context.user_data['metadata']['Details'] = details
    
    inc_type = context.user_data.get('incident_type')
    date = context.user_data.get('incident_date')
    metadata = context.user_data.get('metadata', {})
    
    # Save to DB
    database.save_report(user.id, f"Forensic: {inc_type}", "Metadata in PDF", date)
    
    # Generate PDF
    pdf_filename = f"CyberRescue_Forensic_{user.id}.pdf"
    pdf_generator.generate_report_pdf(user.id, user.username or "User", inc_type, metadata, date, pdf_filename)
    
    # Send PDF
    with open(pdf_filename, "rb") as pdf_file:
        await update.message.reply_document(document=pdf_file, caption="✅ Forensic Report Ready!")
    
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)
        
    # Draft Options
    keyboard = [
        [InlineKeyboardButton("Bank Dispute 🏛️", callback_data="draft_bank")],
        [InlineKeyboardButton("Police Complaint 📝", callback_data="draft_police")],
        [InlineKeyboardButton("Social Media Appeal 📱", callback_data="draft_social")],
        [InlineKeyboardButton("Finish 🏁", callback_data=f"lang_{lang}")]
    ]
    await update.message.reply_text("✍️ Need a specific draft based on these details?", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    return ConversationHandler.END

async def handle_draft_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user
    metadata = context.user_data.get('metadata', {})
    date = context.user_data.get('incident_date', 'N/A')
    
    draft_text = ""
    if data == "draft_bank":
        draft_text = drafter.get_bank_dispute_draft(user.username or "Customer", metadata.get('Platform/Bank', 'Bank'), metadata.get('Amount Lost', '0'), metadata.get('Transaction ID', 'N/A'), date)
    elif data == "draft_police":
        draft_text = drafter.get_police_complaint_draft(user.id, context.user_data.get('incident_type'), date, metadata.get('Details', ''))
    elif data == "draft_social":
        draft_text = drafter.get_social_media_appeal(metadata.get('Platform/Bank', 'Platform'), user.username or "user", date)

    if draft_text:
        await query.message.reply_text(f"📝 *Draft:*\n\n```{draft_text}```", parse_mode='Markdown')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END

# Definition of start_report MUST be visible before report_handler use
async def start_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    msg_text = f"{STRINGS[lang]['report_start']}\n\n*Step 1:* {FORENSIC_QS[lang]['type']}"
    
    context.user_data['metadata'] = {} # Reset metadata
    
    if query:
        await query.answer()
        await query.edit_message_text(msg_text, reply_markup=constants.INCIDENT_TYPES_KB[lang], parse_mode='Markdown')
    else:
        await update.message.reply_text(msg_text, reply_markup=constants.INCIDENT_TYPES_KB[lang], parse_mode='Markdown')
    return INCIDENT_TYPE

# Handler definition moved to END of file
report_handler = ConversationHandler(
    entry_points=[CommandHandler("report", start_report), CallbackQueryHandler(start_report, pattern="^menu_report$")],
    states={
        INCIDENT_TYPE: [CallbackQueryHandler(get_incident_type, pattern="^rep_type_")],
        PLATFORM: [CallbackQueryHandler(get_platform, pattern="^rep_plat_")],
        FINANCIAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fin_amount)],
        FINANCIAL_TXID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fin_txid)],
        ACCOUNT_2FA: [CallbackQueryHandler(get_acc_2fa, pattern="^rep_2fa_")],
        ACCOUNT_REC: [CallbackQueryHandler(get_acc_rec, pattern="^rep_rec_")],
        IDENTITY_SUSPECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_suspect)],
        IDENTITY_DOCS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_docs)],
        DATE_OCCURRED: [
            CallbackQueryHandler(get_date_occurred, pattern="^rep_date_"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_date_occurred)
        ],
        EXTRA_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_extra_details)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import constants
import database
import intel
import tools
import drafter

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    database.save_user(user.id, user.username)
    database.log_activity(user.id, "/start")
    await update.message.reply_text("🌐 Choose your preferred language / अपनी भाषा चुनें:", reply_markup=constants.LANG_KEYBOARD)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    await update.message.reply_text(constants.STRINGS[lang]['help'], parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    data = query.data
    lang = database.get_user_language(user_id)

    if data.startswith("lang_"):
        new_lang = data.split("_")[1]
        database.save_user(user_id, update.effective_user.username, new_lang)
        await query.edit_message_text(constants.STRINGS[new_lang]['start'], reply_markup=constants.get_main_menu(new_lang), parse_mode='Markdown')
    
    elif data == "menu_lang":
        await query.edit_message_text("🌐 Choose your preferred language / अपनी भाषा चुनें:", reply_markup=constants.LANG_KEYBOARD)
    
    elif data == "menu_fir":
        await query.message.reply_text(constants.STRINGS[lang]['fir'], reply_markup=constants.get_portal_button(lang), parse_mode='Markdown')
    
    elif data == "menu_lost":
        await query.message.reply_text(constants.STRINGS[lang]['lost'], parse_mode='Markdown')
    
    elif data == "menu_hacked":
        await query.message.reply_text(constants.STRINGS[lang]['hacked'], parse_mode='Markdown')
    
    elif data == "menu_safe":
        poster_key = random.choice(list(constants.POSTERS.keys()))
        with open(constants.POSTERS[poster_key], 'rb') as photo:
            await query.message.reply_photo(photo=photo, caption=constants.STRINGS[lang]['safe'], parse_mode='Markdown')
    
    elif data == "menu_report":
        from reporting import start_report
        return await start_report(update, context)
    
    elif data == "menu_action":
        keyboard = [
            [InlineKeyboardButton(constants.STRINGS[lang]['btn_scam'], callback_data="action_scam")],
            [InlineKeyboardButton(constants.STRINGS[lang]['btn_checklist'], callback_data="action_checklist")],
            [InlineKeyboardButton(constants.STRINGS[lang]['btn_bank_dir'], callback_data="action_banks")],
            [InlineKeyboardButton("Back ⬅️", callback_data=f"lang_{lang}")]
        ]
        await query.edit_message_text(constants.STRINGS[lang]['action_center'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "action_scam":
        await query.message.reply_text(constants.STRINGS[lang]['scamcheck_prompt'], parse_mode='Markdown')

    elif data == "action_checklist":
        database.init_checklist(user_id)
        await show_checklist(query, user_id, lang)

    elif data.startswith("check_toggle_"):
        step_index = int(data.split("_")[2])
        checklist = database.get_checklist(user_id)
        step_name, current_status = checklist[step_index]
        database.update_checklist_step(user_id, step_name, 1 if current_status == 0 else 0)
        await show_checklist(query, user_id, lang)

    elif data == "action_banks":
        banks = list(tools.BANK_DIRECTORY.keys())
        keyboard = [[InlineKeyboardButton(b, callback_data=f"bank_info_{b}")] for b in banks]
        keyboard.append([InlineKeyboardButton("Back ⬅️", callback_data="menu_action")])
        await query.edit_message_text(constants.STRINGS[lang]['bank_dir_header'], reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("bank_info_"):
        bank = data.split("_")[2]
        info = tools.get_bank_info(bank)
        msg = f"🏛️ *{bank} Emergency Info*\n\n"
        for k, v in info.items():
            msg += f"• *{k}*: `{v}`\n"
        await query.message.reply_text(msg, parse_mode='Markdown')

    elif data == "menu_end":
        await query.edit_message_text(constants.STRINGS[lang]['end_chat'], parse_mode='Markdown')

async def show_checklist(query, user_id, lang):
    checklist = database.get_checklist(user_id)
    keyboard = []
    for i, (step, status) in enumerate(checklist):
        icon = "✅" if status == 1 else "⬜"
        keyboard.append([InlineKeyboardButton(f"{icon} {step}", callback_data=f"check_toggle_{i}")])
    keyboard.append([InlineKeyboardButton("Back ⬅️", callback_data="menu_action")])
    await query.edit_message_text(constants.STRINGS[lang]['checklist_header'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    text = update.message.text
    
    # Check if user is in Action Center -> Scam Check mode
    # (Simplified: if text is long or looks like a number/URL, try scamcheck first)
    if len(text) > 8 and (text.isdigit() or "." in text or "/" in text):
        result = tools.check_scam(text)
        await update.message.reply_text(result, parse_mode='Markdown')
        return

    intent = intel.detect_intent(text)
    if intent:
        class MockQuery:
            def __init__(self, data, message):
                self.data = data
                self.message = message
            async def answer(self): pass
            async def edit_message_text(self, *args, **kwargs):
                await self.message.reply_text(*args, **kwargs)
        update.callback_query = MockQuery(intent, update.message)
        await handle_callback(update, context)
    else:
        await update.message.reply_text("I'm not sure how to help. Try the menu or /start.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    await update.message.reply_text(constants.STRINGS[lang]['end_chat'], parse_mode='Markdown')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats_data = database.get_stats()
    lang = database.get_user_language(update.effective_user.id)
    msg = constants.STRINGS[lang]['stats'].format(users=stats_data['users'], reports=stats_data['reports'], subs=stats_data['subscribers'])
    await update.message.reply_text(msg, parse_mode='Markdown')

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    reports = database.get_user_reports(user_id)
    if not reports:
        await update.message.reply_text(constants.STRINGS[lang]['no_history'])
        return
    msg = constants.STRINGS[lang]['history']
    for r in reports[:5]:
        msg += f"• *{r[0]}* - {r[1]} lost on {r[2]}\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database.subscribe_user(update.effective_user.id)
    lang = database.get_user_language(update.effective_user.id)
    await update.message.reply_text(constants.STRINGS[lang]['subscribed'], parse_mode='Markdown')

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database.unsubscribe_user(update.effective_user.id)
    lang = database.get_user_language(update.effective_user.id)
    await update.message.reply_text(constants.STRINGS[lang]['unsubscribed'], parse_mode='Markdown')

async def daily_tip_job(context: ContextTypes.DEFAULT_TYPE):
    subs = database.get_all_subscribers()
    for user_id in subs:
        try:
            lang = database.get_user_language(user_id)
            poster_key = random.choice(list(constants.POSTERS.keys()))
            with open(constants.POSTERS[poster_key], 'rb') as photo:
                await context.bot.send_photo(chat_id=user_id, photo=photo, caption=f"🔔 *Daily Safety Tip*\n\n{constants.STRINGS[lang]['safe']}", parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Job Error: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception: {context.error}")
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("⚠️ Error. Try /start.")

import os
import logging
from datetime import time
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    filters,
    Defaults
)
from telegram.constants import ParseMode
from dotenv import load_dotenv

import handlers
import reporting
import database

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    database.init_db()
    token = os.getenv("BOT_TOKEN")
    
    # Set default parse mode
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN)
    application = ApplicationBuilder().token(token).defaults(defaults).build()

    # Handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("stop", handlers.stop))
    application.add_handler(CommandHandler("subscribe", handlers.subscribe))
    application.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe))
    application.add_handler(CommandHandler("stats", handlers.stats))
    application.add_handler(CommandHandler("history", handlers.history))
    application.add_handler(CommandHandler("checklist", lambda u, c: handlers.handle_callback(u, c))) # Alias for easy access
    
    application.add_handler(reporting.report_handler)
    # Register drafting callbacks specifically
    application.add_handler(CallbackQueryHandler(reporting.handle_draft_request, pattern="^draft_"))
    application.add_handler(CallbackQueryHandler(handlers.handle_callback))
    
    # Intent detection for free text
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.handle_text))

    application.add_error_handler(handlers.error_handler)

    # Job Queue for Daily Tips (Scheduled for 9 AM)
    job_queue = application.job_queue
    # job_queue.run_daily(handlers.daily_tip_job, time=time(9, 0, 0))
    # For demo purposes, we can run it every 60 seconds if needed, but let's keep it daily
    
    logger.info("CyberRescue Bot v3 is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()

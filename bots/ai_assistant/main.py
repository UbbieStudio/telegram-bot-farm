import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from shared.ai_handler import AIHandler
from shared.logger import get_logger

# Setup
load_dotenv()
logger = get_logger("AI_Assistant_Bot")
ai_handler = AIHandler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your 2026 AI Assistant. Use /mode to choose a brain!")

async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Gemini 2.5 Flash (FREE)", callback_data="set_model:gemini-2.5-flash")],
        [InlineKeyboardButton("🚀 Gemini 3 Pro (Paid Only)", callback_data="set_model:gemini-3-pro-preview")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select an AI model (Flash is recommended for Free Tier):", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split(":")
    if data[0] == "set_model":
        selected_model = data[1]
        ai_handler.set_model(selected_model)
        await query.edit_message_text(text=f"✅ Now using: **{selected_model}**", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text: return
        
    await update.message.reply_chat_action("typing")
    response = await ai_handler.ask(user_text)
    await update.message.reply_text(response)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
    if not token:
        logger.error("No Token Found!")
        exit(1)

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mode", mode_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logger.info("Bot is starting...")
    application.run_polling()
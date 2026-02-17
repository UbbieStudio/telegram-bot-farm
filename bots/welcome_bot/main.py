import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import redis

load_dotenv()

# Connect to the Redis container using the service name from docker-compose
r = redis.Redis(host='redis', port=6379, decode_responses=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    # Increment a counter in Redis
    count = r.incr('greet_count')
    await update.message.reply_text(f"Hello {user}! I am the Welcome Bot. I have greeted {count} people so far.")

if __name__ == '__main__':
    token = os.getenv("WELCOME_BOT_TOKEN")
    if not token:
        print("Error: WELCOME_BOT_TOKEN not found!")
        exit(1)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Welcome Bot is starting...")
    app.run_polling()
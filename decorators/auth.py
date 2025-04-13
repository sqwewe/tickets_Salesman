from telegram import Update
from telegram.ext import CallbackContext
from config.config import Config

def restricted_access(func):
    async def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id not in Config.ALLOWED_USER_IDS:
            await update.message.reply_text("⛔ Доступ запрещен. Вы не авторизованы.")
            return ConversationHandler.END 
        return await func(update, context)
    return wrapper
from telegram import Update
from telegram.ext import CallbackContext
from decorators.auth import restricted_access
@restricted_access
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}!\n"
        "Я бот для создания заявок. Используй команду /new для создания новой заявки."
    )
@restricted_access
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/new - создать новую заявку\n"
        "/help - получить справку"
    )
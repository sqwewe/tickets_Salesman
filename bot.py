from telegram.ext import (
    Updater,  # Используем Updater вместо Application
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters  # С большой буквы в версии 13.7
)
from config.config import Config
from handlers.start import start, help_command
from handlers.tickets import (
    start_ticket_creation, get_reason, get_info, get_phone,
    confirm_ticket, cancel,
    GETTING_REASON, GETTING_INFO, GETTING_PHONE, CONFIRMATION
)

def main():
    # Используем Updater для версии 13.7
    updater = Updater(Config.TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем проверку авторизации
    def check_access(update):
        user_id = update.effective_user.id
        if user_id not in Config.ALLOWED_USER_IDS:
            update.message.reply_text("⛔ Доступ запрещен. Вы не авторизованы.")
            return False
        return True

    # Обычные команды с проверкой доступа
    def wrapped_start(update, context):
        if not check_access(update):
            return
        return start(update, context)

    def wrapped_help(update, context):
        if not check_access(update):
            return
        return help_command(update, context)

    dp.add_handler(CommandHandler("start", wrapped_start))
    dp.add_handler(CommandHandler("help", wrapped_help))
    
    # ConversationHandler с проверкой в каждом обработчике
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', start_ticket_creation)],
        states={
            GETTING_REASON: [MessageHandler(Filters.text & ~Filters.command, get_reason)],
            GETTING_INFO: [MessageHandler(Filters.text & ~Filters.command, get_info)],
            GETTING_PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
            CONFIRMATION: [MessageHandler(Filters.regex('^(Да|Нет)$'), confirm_ticket)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
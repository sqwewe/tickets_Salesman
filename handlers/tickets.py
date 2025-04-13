from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from models.ticket import Ticket
from config.config import Config


# States for conversation
(
    GETTING_REASON,
    GETTING_INFO,
    GETTING_PHONE,
    CONFIRMATION
) = range(4)
def check_access(update):
    user_id = update.effective_user.id
    if user_id not in Config.ALLOWED_USER_IDS:
        update.message.reply_text("⛔ Доступ запрещен")
        return False
    return True

def start_ticket_creation(update: Update, context: CallbackContext) -> int:
    if not check_access(update):
        return ConversationHandler.END
   
def start_ticket_creation(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Новое подключение', 'Другая причина']]
    
    update.message.reply_text(
        "Выберите причину заявки:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder='Причина заявки'
        ),
    )
    
    return GETTING_REASON

def get_reason(update: Update, context: CallbackContext) -> int:
    reason = update.message.text
    if reason == 'Другая причина':
        update.message.reply_text(
            "Укажите свою причину:",
            reply_markup=ReplyKeyboardRemove(),
        )
        return GETTING_REASON
    
    context.user_data['reason_text'] = reason
    context.user_data['reason_id'] = 2  
    
    update.message.reply_text(
        "Укажите адрес или другую важную информацию:",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return GETTING_INFO

def get_info(update: Update, context: CallbackContext) -> int:
    context.user_data['info'] = update.message.text
    
    update.message.reply_text(
        "Укажите контактный телефон:",
    )
    
    return GETTING_PHONE

def get_phone(update: Update, context: CallbackContext) -> int:
    phone = update.message.text
    if not phone.replace('+', '').isdigit():
        update.message.reply_text("Пожалуйста, введите корректный номер телефона.")
        return GETTING_PHONE
    
    context.user_data['phone'] = phone
    
    summary = (
        "Проверьте данные заявки:\n\n"
        f"Причина: {context.user_data.get('reason_text')}\n"
        f"Адрес/инфо: {context.user_data.get('info')}\n"
        f"Телефон: {phone}\n\n"
        "Всё верно?"
    )
    
    reply_keyboard = [['Да', 'Нет']]
    update.message.reply_text(
        summary,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    
    return CONFIRMATION

def confirm_ticket(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'нет':
        update.message.reply_text(
            "Заявка отменена. Начните заново, если нужно.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    
    ticket_data = {
        'user_id': update.effective_user.id,
        'reason_text': context.user_data.get('reason_text'),
        'info': context.user_data.get('info'),
        'phone': context.user_data.get('phone'),
    }
    
    ticket = Ticket(ticket_data)
    created_ticket = Ticket.create(ticket)
    
    update.message.reply_text(
        f"Заявка #{created_ticket.id} успешно создана!",
        reply_markup=ReplyKeyboardRemove(),
    )
    
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Создание заявки отменено.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

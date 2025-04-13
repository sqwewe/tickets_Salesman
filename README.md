# tickets_Salesman
Бот создан для автоматизации работы продажников и абонентского отдела, с помощью данного бота, продажники могут создавать заявки напрямую в CRM систему
Bot for Salesman/

├── config/ config.py          # Конфигурационные параметры

├── database/ db_connection.py   # Подключение к БД

├── handlers/ start.py           # Команды start, help
| tickets.py         # Логика работы с заявками
| auth.py            # Проверка авторизации

├── models/ ticket.py          # Модель заявки

├── utils/ decorators.py      # Декораторы (например, для проверки доступа) | logger.py          # Настройка логгирования

├── .env                   # Переменные окружения (ниже описаны нужные переменные)

├── requirements.txt       # Зависимости bot.py                 # Главный файл бота

*env
TELEGRAM_BOT_TOKEN = Токен нашего бота
ALLOWED_USER_IDS = id telegram: для авторизации от левых пользователей 
DB_HOST - хост БД
DB_PORT - порт БД
DB_USER - юзер БД
DB_PASSWORD - пароль юзера БД
DB_NAME - название БД

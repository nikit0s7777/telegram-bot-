import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Импорт обработчиков
from handlers.start import start_command, handle_message
from handlers.catalog import show_services, handle_service_selection
from handlers.orders import handle_order_description, handle_contact_info, show_user_orders
from handlers.language import change_language, show_language_menu

load_dotenv()

def main():
    # Создаем приложение
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    
    # Обработчик смены языка
    application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
    
    # Обработчик инлайн-кнопок (каталог услуг)
    application.add_handler(CallbackQueryHandler(handle_service_selection))
    
    # Обработчик описания заказа (должен быть перед общим обработчиком сообщений)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_order_description,
        block=False
    ))
    
    # Общий обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()

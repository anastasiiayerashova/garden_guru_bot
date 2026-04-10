import os
import logging
from dotenv import load_dotenv
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

from services import get_agent_response
from logger_config import setup_logging
from handlers import start_command, exit_command, help_command, calc_command, guide_command, error_handler


load_dotenv()
setup_logging()
logger = setup_logging()


async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id
    session_id = context.user_data.get('session_id', 0)

    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    try:
        response = await get_agent_response(user_text, chat_id, session_id)

        # sending response to tg
        if response:
            logger.info(f'Відповідь агента для чату {chat_id}: {response[:50]}...')
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            logger.warning('Отримано порожню відповідь від агента.')
            await update.message.reply_text('Вибачте, не вдалося отримати відповідь. Спробуйте ще раз.')

    except Exception as e:
        logger.error(f'Помилка при отриманні відповіді: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася внутрішня помилка. Спробуйте пізніше.')


# launching

if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    PORT = os.getenv('PORT', 8000)
    RENDER_EXTERNAL_URL = os.getenv('RENDER_EXTERNAL_URL')

    if not TELEGRAM_TOKEN:
        logger.error('Помилка: TELEGRAM_TOKEN не знайдено в .env файлі.')

    else:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).connect_timeout(30).read_timeout(30).build()
        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('exit', exit_command))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CommandHandler('calc', calc_command))
        app.add_handler(CommandHandler('guide', guide_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_telegram_message))
        app.add_error_handler(error_handler)

        if RENDER_EXTERNAL_URL:
            logger.info(f'Запускаємо бота на Render з портом {PORT}...')
            app.run_webhook(
                listen='0.0.0.0', 
                port=int(PORT), 
                url_path=TELEGRAM_TOKEN, 
                webhook_url=f'{RENDER_EXTERNAL_URL}/{TELEGRAM_TOKEN}'
            )
        else:
            logger.info('Запускаємо бота в режимі довгого опитування (polling)...')
            app.run_polling()










# async def start_terminal_chat():
#     session_id = str(uuid.uuid4())
    
#     print('🌿 Ласкаво просимо до GardenGuru (Terminal Mode)!')
#     print('Введіть "вихід", щоб завершити розмову.\n')

#     while True:
#         user_input = input('👤 Ви: ')

#         if user_input.lower() in ['вихід', 'exit', 'quit']:
#             print('🧤 Садівник пішов відпочивати. До зустрічі!')
#             break

#         if not user_input.strip():
#             continue

#         logger.info(f'Отримано запит: {user_input[:30]}...')
#         print('🤖 GardenGuru думає...')

#         try:
#             response = await get_agent_response(user_input, chat_id=hash(session_id))
            
#             if response:
#                 print(f'\n🌻 GardenGuru: {response}\n')

#             else:
#                 logger.warning('Отримано порожню відповідь від агента.')
#                 print('\n❌ Помилка: Не вдалося отримати відповідь.\n')
                
#         except Exception as e:
#             logger.error(f'Помилка при отриманні відповіді: {e}', exc_info=True)

# if __name__ == '__main__':
#     try:
#         asyncio.run(start_terminal_chat())

#     except KeyboardInterrupt:
#         print('\nЧат перервано користувачем.')
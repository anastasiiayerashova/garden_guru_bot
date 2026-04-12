import os
import logging
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from logger_config import setup_logging
from handlers import router as handlers_router
from handlers import set_commands


load_dotenv()
setup_logging()
logger = setup_logging()



async def main():
    telegram_token = os.getenv('TELEGRAM_TOKEN')

    if not telegram_token:
        logger.error('Помилка: TELEGRAM_TOKEN не знайдено в .env файлі.')
        return

    bot = Bot(
        token=telegram_token, 
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(handlers_router)


    try:
        await set_commands(bot)
        logger.info("✅ Список команд успішно оновлено.")

    except Exception as e:
        logger.error(f'Помилка при встановленні команд: {e}', exc_info=True)


    logger.info("🚀 Запуск GardenGuru в режимі Polling...")


    try:
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f'Помилка при запуску бота: {e}', exc_info=True)
    
    finally:
        await bot.session.close()

    
if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt):
        logger.info('Бот зупинено вручну (KeyboardInterrupt).')
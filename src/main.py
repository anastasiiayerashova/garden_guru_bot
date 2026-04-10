import os
import logging
from dotenv import load_dotenv
import asyncio
import uuid

from services import get_agent_response
from logger_config import setup_logging


load_dotenv()
setup_logging()
logger = setup_logging()


async def start_terminal_chat():
    session_id = str(uuid.uuid4())
    
    print('🌿 Ласкаво просимо до GardenGuru (Terminal Mode)!')
    print('Введіть "вихід", щоб завершити розмову.\n')

    while True:
        user_input = input('👤 Ви: ')

        if user_input.lower() in ['вихід', 'exit', 'quit']:
            print('🧤 Садівник пішов відпочивати. До зустрічі!')
            break

        if not user_input.strip():
            continue

        logger.info(f'Отримано запит: {user_input[:30]}...')
        print('🤖 GardenGuru думає...')

        try:
            response = await get_agent_response(user_input, chat_id=hash(session_id))
            
            if response:
                print(f'\n🌻 GardenGuru: {response}\n')

            else:
                logger.warning('Отримано порожню відповідь від агента.')
                print('\n❌ Помилка: Не вдалося отримати відповідь.\n')
                
        except Exception as e:
            logger.error(f'Помилка при отриманні відповіді: {e}', exc_info=True)

if __name__ == '__main__':
    try:
        asyncio.run(start_terminal_chat())

    except KeyboardInterrupt:
        print('\nЧат перервано користувачем.')
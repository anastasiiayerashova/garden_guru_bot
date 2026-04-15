
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand
import os
import logging
import time

from services import get_agent_response
from vision_services import identify_plant, identify_disease
from utils import command_help_text, command_calc_text, command_guide_text, command_identify_text, command_disease_text

logger = logging.getLogger(__name__)
router = Router()


# command handlers for Telegram bot

@router.message(Command('start'))
async def start_command(message: Message):
    '''Надсилає привітальне повідомлення, коли користувач натискає /start'''

    user_name = message.from_user.first_name

    welcome_text = (
        f'Привіт, {user_name}! 👋\n\n' \
        'Я — **GardenGuru** 🌿, твій персональний асистент-садівник та експерт із фітопатології.\n\n' \
        '**Що я вмію:**\n' \
        '• Даю поради з догляду на основі власної бази знань 📖\n' \
        '• Діагностую хвороби та підбираю лікування 🍎\n' \
        '• Допомагаю з розрахунками добрив через калькулятор 🧮\n' \
        '• Складаю календар посадок саме для твоїх рослин 📅\n\n' \
        'Розкажи, що у тебе росте, або постав будь-яке садове питання. Чим допоможу сьогодні? 🌱'
    )

    try:
        logger.info('handler /start')
        await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /start: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /start. Спробуйте ще раз.')



@router.message(Command('exit'))
async def exit_command(message: Message, state: FSMContext):
    '''Очищує контекст та прощається з користувачем'''
    
    data = await state.get_data()
    current_session = data.get('session_id', 0)

    new_session = current_session + 1
    await state.update_data(session_id=new_session)
    
    exit_text = (
        'Сесію завершено! 👋\n\n' \
        "Я очистив історію нашого листування. Моя 'пам’ять' тепер чиста, як щойно зорана грядка. 🌿\n\n" \
        'Якщо знову знадобиться порада щодо рослин — просто напиши мені або натисни /start. Гарного дня! 🌱☀️'
        f'Поточна сесія: {new_session}. Якщо знадобиться порада — пиши!'
    )

    try:
        logger.info('handler /exit')
        await message.answer(exit_text)

    except Exception as e:
        logger.error(f'Помилка в команді /exit: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /exit. Спробуйте ще раз.')



@router.message(Command('help'))
async def help_command(message: Message):
    '''Пояснює користувачеві можливості бота'''

    help_text = command_help_text

    try:
        logger.info('handler /help')
        await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /help: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /help. Спробуйте ще раз.')



@router.message(Command('calc'))
async def calc_command(message: Message):
    '''Пояснює, як користуватися калькулятором'''

    calc_text = command_calc_text

    try:
        logger.info('handler /calc')
        await message.answer(calc_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /calc: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /calc. Спробуйте ще раз.')



@router.message(Command('guide'))
async def guide_command(message: Message):
    '''Пояснює, як працює пошук знань'''

    guide_text = command_guide_text

    try:
        logger.info('handler /guide')
        await message.answer(guide_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /guide: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /guide. Спробуйте ще раз.')



@router.message(Command('identify'))
async def identify_command(message: Message):
    '''Пояснює, як працює розпізнавання рослин по фото'''

    identify_text = command_identify_text

    try:
        logger.info('handler /identify')
        await message.answer(identify_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /identify: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /identify. Спробуйте ще раз.')



@router.message(Command('disease'))
async def disease_command(message: Message):
    '''Пояснює, як працює діагностика хвороб'''
    
    disease_text = command_disease_text
    
    try:
        logger.info('handler /disease')
        await message.answer(disease_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /disease: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /disease. Спробуйте ще раз.')



@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    user_input = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id

    data = await state.get_data()
    session_id = data.get('session_id', 0)

    logger.info(f'USER[{user_id}] запит: "{user_input[:30]}..." (Session: {session_id})')

    await message.bot.send_chat_action(chat_id=chat_id, action='typing')

    start_time = time.perf_counter()

    try:
        response = await get_agent_response(user_input, chat_id, session_id)

        duration = time.perf_counter() - start_time

        if response:
            logger.info(f'Відповідь агента для чату {chat_id} | USER[{user_id}] | Time: {duration:.2f}с | Response: {response[:50]}...')
            await message.answer(response, parse_mode=ParseMode.MARKDOWN)

        else:
            logger.warning(f'Отримано порожню відповідь від агента для USER[{user_id}].')
            await message.answer('Вибачте, не вдалося отримати відповідь. Спробуйте ще раз.')

    except Exception as e:
        duration = time.perf_counter() - start_time
        logger.error(f'Для USER[{user_id}] помилка через {duration:.2f}с при отриманні відповіді: {e}', exc_info=True)
        await message.answer('Вибачте, сталася внутрішня помилка. Спробуйте пізніше.')



@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]

    logger.info(f'USER[{user_id}] надіслав фото на аналіз. File_id: {photo.file_id}')
    start_total = time.perf_counter()

    file_info = await message.bot.get_file(photo.file_id)

    image_name = f'temp_{user_id}_{photo.file_id}.jpg'

    status_msg = await message.answer('🔍 Дивлюсь на фото... Зараз розпізнаю рослину.')


    try:
        await message.bot.download_file(file_info.file_path, image_name)
        logger.debug(f'USER[{user_id}] фото завантажено як {image_name}')

        start_step = time.perf_counter()

        identification_result = await identify_plant(image_name)

        logger.info(f'USER[{user_id}] ідентифікація рослини ({time.perf_counter() - start_step:.2f}с): {identification_result}')

        await status_msg.edit_text(f'✅ {identification_result}\n\nТепер перевіряю на наявність хвороб... 🏥')

        start_step = time.perf_counter()

        disease_result = await identify_disease(image_name)

        logger.info(f'USER[{user_id}] діагностика хвороби ({time.perf_counter() - start_step:.2f}с): {disease_result}')

        await status_msg.edit_text(
            f'✅ {identification_result}\n'
            f'{disease_result}\n\n'
            f'Звертаюся до експертної бази знань за порадами... 📖'
        )

        prompt = (
            f'Користувач надіслав фото. Аналіз Pl@ntNet:\n'
            f'- Вид рослини: {identification_result}\n'
            f'- Ймовірна хвороба: {disease_result}\n\n'
            'Використовуй свої внутрішні знання, щоб підтвердити або спростувати цей діагноз.'
            'Якщо API повернуло "Рослину не вдалося визначити. Спробуйте інше зображення." або "Вибачте, не вдалося визначити хворобу. Спробуйте ще раз пізніше.", ввічливо скажи що на фото імовірно не рослина'
            'Якщо API повернуло скорочену назву шкідника (наприклад, LPTNDE), розшифруй її та дай рекомендації по боротьбі.'
            'ВИМОГА: Знайди в базі знань GardenGuru правила догляду для цієї рослини.'
            'НЕ використовуй semantic_search для діагностики хвороби, спирайся на свої знання про хвороби рослин.'
            "1. Розшифруй латинську назву або технічний код патології.\n"
            "2. На основі своїх знань поясни користувачеві, що це і як лікувати.\n"
            "3. Якщо це шкідник, опиши його життєвий цикл і засоби боротьби."
        )

        start_step = time.perf_counter()

        agent_answer = await get_agent_response(
            user_text=prompt, 
            chat_id=message.chat.id
        )

        duration_agent = time.perf_counter() - start_step
        logger.info(f'USER[{user_id}] відповідь агента отримана за {duration_agent:.2f}с')

        await status_msg.edit_text(agent_answer, parse_mode='Markdown')

        total_duration = time.perf_counter() - start_total
        logger.info(f'USER[{user_id}] ПОВНИЙ ЦИКЛ ОБРОБКИ ФОТО ЗАВЕРШЕНО за {total_duration:.2f}с')


    except Exception as e:
        total_duration = time.perf_counter() - start_total
        logger.error(f'USER[{user_id}] помилка при обробці фото через {total_duration:.2f}с: {e}', exc_info=True)
        await status_msg.edit_text('❌ Вибачте, не вдалося проаналізувати фото. Спробуйте ще раз або напишіть назву текстом.')


    finally:
        if os.path.exists(image_name):
            os.remove(image_name)
            logger.debug(f'USER[{user_id}] тимчасовий файл {image_name} видалено')



async def set_commands(bot):
    commands = [
        BotCommand(command='start', description='Почати роботу з ботом'),
        BotCommand(command='help', description='Показати довідку по використанню бота'),
        BotCommand(command='identify', description='Дізнатися, як розпізнати рослину за фото'),
        BotCommand(command='disease', description='Діагностика хвороби 🏥'),
        BotCommand(command='calc', description='Дізнатися, як користуватися калькулятором'),
        BotCommand(command='guide', description='Отримати поради щодо догляду та діагностики'),
        BotCommand(command='exit', description='Очистити історію та почати з чистого листа')
    ]

    try:
        await bot.set_my_commands(commands)

    except Exception as e:
        logger.error(f'Помилка при встановленні команд бота: {e}', exc_info=True)
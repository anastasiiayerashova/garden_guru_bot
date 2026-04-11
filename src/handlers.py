
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
import logging

from logger_config import setup_logging
from services import get_agent_response

logger = logging.getLogger(__name__)
router = Router()

# Command handlers for Telegram bot

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
        await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /start: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася помилка при відправці команди /start. Спробуйте ще раз.')



@router.message(Command('exit'))
async def exit_command(message: Message, state: FSMContext):
    '''Очищує контекст та прощається з користувачем'''
    
    data = await state.get_data()
    current_session = data.get('session_id', 0)

    new_session = current_session + 1
    await state.update_data(session_id=new_session)
    

    exit_text = (
        'Сесію завершено! 👋\n\n' \
        'Я очистив історію нашого листування. Моя "пам’ять" тепер чиста, як щойно зорана грядка. 🌿\n\n' \
        'Якщо знову знадобиться порада щодо рослин — просто напиши мені або натисни /start. Гарного дня! 🌱☀️'
        f'Поточна сесія: {new_session}. Якщо знадобиться порада — пиши!'
    )
    try:
        await message.answer(exit_text)

    except Exception as e:
        logger.error(f'Помилка в команді /exit: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася помилка при відправці команди /exit. Спробуйте ще раз.')



@router.message(Command('help'))
async def help_command(message: Message):
    '''Пояснює користувачеві можливості бота'''

    help_text = (
        '🤖 **Як користуватися GardenGuru?**\n\n' \
        'Я твій персональний садовий експерт. Просто пиши мені запитання про свої рослини, ' \
        'а я використовуватиму свою базу знань та інструменти для точних порад.\n\n' \
        '✨ **Що я вмію:**\n' \
        '• **Енциклопедія:** Запитай про догляд, наприклад: `Як поливати фіалку?` — я знайду це у своїй базі знань. 📖\n' \
        '• **Діагностика:** Опиши проблему, наприклад: `Чому жовтіє листя у томатів?` — я допоможу знайти причину. 🔍\n' \
        '• **Розрахунки:** Напиши `Скільки добрива потрібно на 5 кв.м?` — і я використаю калькулятор. 🧮\n' \
        '• **Календар:** Запитай `Коли садити помідори?`, щоб отримати оптимальні дати. 📅\n\n' \
        '📝 **Команди:**\n' \
        '/start — почати знайомство та роботу\n' \
        '/calc — як користуватися калькулятором добрив\n' \
        '/guide — отримати поради щодо діагностики рослин\n' \
        '/exit — очистити історію та почати з чистого листа\n' \
        '/help — показати цю довідку\n\n' \
        '💡 *Порада: якщо у тебе є фото хворої рослини — опиши симптоми максимально детально!* 🌿'
    )
    try:
        await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /help: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася помилка при відправці команди /help. Спробуйте ще раз.')



@router.message(Command('calc'))
async def calc_command(message: Message):
    '''Пояснює, як користуватися калькулятором'''

    calc_help = (
        '🧮 **Калькулятор садівника**\n\n' \
        'Я допоможу тобі розрахувати норми внесення добрив або площу ділянки. ' \
        'Тобі не потрібно рахувати вручну — просто напиши умови!\n\n' \
        '📝 **Приклади запитів:**\n' \
        '• "У мене ділянка 2 на 4 метри, скільки це квадратних метрів?"\n' \
        '• "Норма добрива 20г на 1 кв.м. Скільки потрібно добрива на 15 кв.м?"\n' \
        '• "Скільки води потрібно для поливу 50 кущів, якщо на один йде 3 літри?"\n\n' \
        '💡 *Порада: вказуй цифри та одиниці виміру (метри, грами, літри), і я миттєво дам відповідь!*'
    )
    try:
        await message.answer(calc_help, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /calc: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася помилка при відправці команди /calc. Спробуйте ще раз.')



@router.message(Command('guide'))
async def guide_command(message: Message):
    '''Пояснює, як працює пошук знань'''

    guide_help = (
        '📖 **Гід з догляду та діагностики**\n\n' \
        'Я маю доступ до спеціалізованої бази знань GardenGuru. Щоб я міг знайти ' \
        'найкращу пораду, описуй проблему детально.\n\n' \
        '🔍 **Як запитувати:**\n' \
        '• **Для догляду:** "Який світловий режим потрібен для фіалки?" або "Як правильно підживлювати огірки?"\n' \
        '• **Для діагностики:** "На листі помідорів з’явилися бурі плями, що це може бути?"\n\n' \
        '🌿 Якщо я знайду інформацію в енциклопедії, я обов’язково пошлюся на неї у відповіді. Якщо ж питання загальне — відповім на основі своїх знань.'
    )
    try:
        await message.answer(guide_help, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /guide: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася помилка при відправці команди /guide. Спробуйте ще раз.')



@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    user_input = message.text
    chat_id = message.chat.id

    data = await state.get_data()
    session_id = data.get('session_id', 0)

    await message.bot.send_chat_action(chat_id=chat_id, action='typing')

    try:
        response = await get_agent_response(user_input, chat_id, session_id)

        if response:
            logger.info(f'Відповідь агента для чату {chat_id}: {response[:50]}...')
            await message.answer(response, parse_mode=ParseMode.MARKDOWN)

        else:
            logger.warning('Отримано порожню відповідь від агента.')
            await message.reply_text('Вибачте, не вдалося отримати відповідь. Спробуйте ще раз.')

    except Exception as e:
        logger.error(f'Помилка при отриманні відповіді: {e}', exc_info=True)
        await message.reply_text('Вибачте, сталася внутрішня помилка. Спробуйте пізніше.')
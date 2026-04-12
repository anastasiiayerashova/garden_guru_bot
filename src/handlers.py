
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand
import logging
import os

from logger_config import setup_logging
from services import get_agent_response
from vision_services import identify_plant, identify_disease

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
        await message.answer(exit_text)

    except Exception as e:
        logger.error(f'Помилка в команді /exit: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /exit. Спробуйте ще раз.')



@router.message(Command('help'))
async def help_command(message: Message):
    '''Пояснює користувачеві можливості бота'''

    help_text = (
        '🤖 **Як користуватися GardenGuru?**\n\n' \
        'Я твій персональний садовий експерт. Просто пиши мені запитання про свої рослини, ' \
        'а я використовуватиму свою базу знань та інструменти для точних порад.\n\n' \
        '✨ **Що я вмію:**\n' \
        '• **Енциклопедія:** Запитай про догляд, наприклад: `Як поливати фіалку?` — я знайду це у своїй базі знань. 📖\n' \
        '• **Фото-ідентифікація:** Надішли мені фото рослини, і я розпізнаю її вид за допомогою нейромережі **Pl@ntNet API**. 📸\n'
        '• **Діагностика:** Опиши проблему, наприклад: \n`Чому жовтіє листя у томатів?` — я допоможу знайти причину. 🔍\n' \
        '• **Розрахунки:** Напиши: \n`Скільки добрива потрібно на 5 кв.м?` — і я використаю калькулятор. 🧮\n' \
        '• **Календар:** Запитай: \n`Коли садити помідори?`, щоб отримати оптимальні дати. 📅\n\n' \
        '📝 **Команди:**\n' \
        '/start — почати знайомство та роботу\n' \
        '/identify — як розпізнати рослину за фото\n'
        '/disease — як провести діагностику хвороби за фото\n'
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
        await message.answer('Вибачте, сталася помилка при відправці команди /help. Спробуйте ще раз.')



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
        await message.answer('Вибачте, сталася помилка при відправці команди /calc. Спробуйте ще раз.')



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
        await message.answer('Вибачте, сталася помилка при відправці команди /guide. Спробуйте ще раз.')



@router.message(Command('identify'))
async def identify_command(message: Message):
    '''Пояснює, як працює розпізнавання рослин по фото'''

    identify_text = (
        '📸 **Фото-ідентифікація рослин**\n\n'
        'Я використовую технологію **Pl@ntNet API** — одну з найпотужніших систем '
        "комп'ютерного зору у світі, яка базується на наукових базах даних.\n\n"
        '✨ **Як це працює:**\n'
        '1. Ви надсилаєте фото.\n'
        '2. Алгоритми Pl@ntNet порівнюють його з тисячами видів.\n'
        '3. Я отримую назву та шукаю поради щодо догляду саме за цією рослиною.\n\n'
        '💡 **Порада:** для найкращого результату фотографуйте окремі частини рослини '
        '(квітку або листок) крупним планом.'
    )

    try:
        await message.answer(identify_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f'Помилка в команді /identify: {e}', exc_info=True)
        await message.answer('Вибачте, сталася помилка при відправці команди /identify. Спробуйте ще раз.')



@router.message(Command('disease'))
async def disease_command(message: Message):
    '''Пояснює, як працює діагностика хвороб'''
    text = (
        '🏥 **Діагностика хвороб за фото**\n\n'
        'Я допоможу визначити, що з твоїм зеленим другом, використовуючи професійні алгоритми **Pl@ntNet API**! 🌿\n\n'
        '✨ **Як це працює:**\n'
        '1. Надішли фото ураженої ділянки (плями на листі, наліт, шкідники).\n'
        '2. Нейромережа **Pl@ntNet** проаналізує візуальні симптоми серед тисяч відомих патологій.\n'
        '3. Я отримаю результат і надам тобі поради щодо лікування з власної бази знань. 📖\n\n'
        '💡 **Порада:** роби фото при гарному освітленні та максимально близько до проблеми (макрозйомка), щоб я міг розгледіти деталі.'
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)



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
            await message.answer('Вибачте, не вдалося отримати відповідь. Спробуйте ще раз.')

    except Exception as e:
        logger.error(f'Помилка при отриманні відповіді: {e}', exc_info=True)
        await message.answer('Вибачте, сталася внутрішня помилка. Спробуйте пізніше.')



@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_info = await message.bot.get_file(photo.file_id)

    image_name = f'temp_{photo.file_id}.jpg'

    status_msg = await message.answer('🔍 Дивлюсь на фото... Зараз розпізнаю рослину.')

    try:
        await message.bot.download_file(file_info.file_path, image_name)

        identification_result = await identify_plant(image_name)
        await status_msg.edit_text(f'✅ {identification_result}\n\nТепер перевіряю на наявність хвороб... 🏥')

        disease_result = await identify_disease(image_name)

        await status_msg.edit_text(
            f'✅ {identification_result}\n'
            f'{disease_result}\n\n'
            f'Звертаюся до експертної бази знань за порадами... 📖'
        )

        prompt = (
            f'Користувач надіслав фото. Аналіз Pl@ntNet:\n'
            f'- Вид рослини: {identification_result}\n'
            f'- Ймовірна хвороба: {disease_result}\n\n'
            'Використовуй ці дані та інструмент semantic_search, щоб надати:'
            '1. Коротку довідку про догляд за цією рослиною.'
            '2. Підтвердження або уточнення діагнозу хвороби.'
            '3. Конкретні кроки для лікування (препарати або догляд).'
        )

        agent_answer = await get_agent_response(
            user_text=prompt, 
            chat_id=message.chat.id
        )

        await status_msg.edit_text(agent_answer, parse_mode='Markdown')

    except Exception as e:
        await status_msg.edit_text('❌ Вибачте, не вдалося проаналізувати фото. Спробуйте ще раз або напишіть назву текстом.')
        logger.error(f'Помилка при обробці фото: {e}', exc_info=True)

    finally:
        if os.path.exists(image_name):
            os.remove(image_name)



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
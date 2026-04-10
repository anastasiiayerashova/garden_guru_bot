from telegram import Update
from telegram.ext import ContextTypes

from logger_config import setup_logging

logger = setup_logging()

# Command handlers for Telegram bot

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Надсилає привітальне повідомлення, коли користувач натискає /start'''

    user_name = update.message.from_user.first_name
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
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    except Exception as e:
        logger.error(f'Помилка в команді /start: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася помилка при відправці команди /start. Спробуйте ще раз.')



async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Очищує контекст та прощається з користувачем'''
    
    current_session = context.user_data.get('session_id', 0)
    context.user_data['session_id'] = current_session + 1

    welcome_text = (
        'Сесію завершено! 👋\n\n' \
        'Я очистив історію нашого листування. Моя "пам’ять" тепер чиста, як щойно зорана грядка. 🌿\n\n' \
        'Якщо знову знадобиться порада щодо рослин — просто напиши мені або натисни /start. Гарного дня! 🌱☀️'
    )
    try:
        await update.message.reply_text(welcome_text)

    except Exception as e:
        logger.error(f'Помилка в команді /exit: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася помилка при відправці команди /exit. Спробуйте ще раз.')



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(help_text, parse_mode='Markdown')

    except Exception as e:
        logger.error(f'Помилка в команді /help: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася помилка при відправці команди /help. Спробуйте ще раз.')



async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(calc_help, parse_mode='Markdown')

    except Exception as e:
        logger.error(f'Помилка в команді /calc: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася помилка при відправці команди /calc. Спробуйте ще раз.')



async def guide_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(guide_help, parse_mode='Markdown')

    except Exception as e:
        logger.error(f'Помилка в команді /guide: {e}', exc_info=True)
        await update.message.reply_text('Вибачте, сталася помилка при відправці команди /guide. Спробуйте ще раз.')


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f'Exception while handling an update: {context.error}', exc_info=True)
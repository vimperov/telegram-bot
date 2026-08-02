import asyncio
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8898626331:AAEHVDoej0mQl-nFmnz2z0vJKTf-GKfAmU"

# Создаём объект бота
application = ApplicationBuilder().token(TOKEN).build()

# ----------------------------------------
# ВАШИ ОБРАБОТЧИКИ КОМАНД (оставляем как есть)
# ----------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот успешно запущен и работает!")

application.add_handler(CommandHandler("start", start))

# ... (остальные ваши add_handler команды) ...

# ----------------------------------------
# ИДЕАЛЬНЫЙ ЗАПУСК ДЛЯ PYTHON 3.14
# ----------------------------------------
async def run_bot():
    # Мы принудительно создаём цикл событий ДО запуска библиотеки
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        await application.run_polling()
    finally:
        loop.close()

def start_bot():
    asyncio.run(run_bot())

if __name__ == '__main__':
    start_bot()
    
# Ваши обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот запущен!")

# Кэш и состояния
cache = {}
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие с красивым меню"""
    welcome_text = (
        "🔍 *Добро пожаловать в OSINT-Бот!*\n\n"
        "🛡️ Я помогу тебе найти информацию по номеру телефона\n"
        "📱 Использую передовые инструменты OSINT\n\n"
        "⚡️ *Выбери действие ниже:*"
    )

    keyboard = [
        [InlineKeyboardButton("🔎 OSINT-поиск", callback_data="osint_search")],
        [InlineKeyboardButton("🏓 Проверить пинг", callback_data="ping")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == "osint_search":
        await query.edit_message_text(
            "📱 *Введите номер телефона для поиска*\n\n"
            "Пример: `+79991234567`\n\n"
            "⏳ Поиск может занять до 30 секунд\n"
            "❌ Для отмены отправь /cancel",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )
        user_states[user_id] = "awaiting_phone"

    elif query.data == "ping":
        start_time = time.time()
        await query.edit_message_text(
            "🏓 *Измеряем пинг...*\n⏳ Пожалуйста, подожди...",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.1)
        end_time = time.time()
        ping_ms = (end_time - start_time) * 1000

        ping_text = (
            f"🏓 *Результат пинг-теста*\n\n"
            f"📡 Пинг: `{ping_ms:.1f} мс`\n"
            f"🕐 Время: `{datetime.now().strftime('%H:%M:%S')}`\n\n"
            f"{'🟢 Отлично!' if ping_ms < 100 else '🟡 Нормально' if ping_ms < 300 else '🔴 Медленно'}"
        )
        await query.edit_message_text(
            ping_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Проверить снова", callback_data="ping")],
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    elif query.data == "about":
        about_text = (
            "ℹ️ *О боте*\n\n"
            "🤖 *Версия:* 2.1\n"
            "🛠️ *Инструменты:* OSINT\n"
            "📱 *Функции:* Поиск по номеру, пинг\n\n"
            "⚡️ *Сделано с ❤️ для OSINT-сообщества*"
        )
        await query.edit_message_text(
            about_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    elif query.data == "contacts":
        contacts_text = (
            "📞 *Контакты*\n\n"
            "👨‍💻 *Разработчик:* @vimperr\n"
            "📧 *Email:* your@email.com\n"
            "💬 *Предложения и вопросы:*\nВсегда рад обратной связи!"
        )
        await query.edit_message_text(
            contacts_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
            ])
        )

    elif query.data == "back_to_menu":
        await show_menu(query)

async def show_menu(query):
    """Показывает главное меню"""
    menu_text = "🔍 *Главное меню*\n\n🛡️ Выбери действие:"
    keyboard = [
        [InlineKeyboardButton("🔎 OSINT-поиск", callback_data="osint_search")],
        [InlineKeyboardButton("🏓 Проверить пинг", callback_data="ping")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await query.edit_message_text(menu_text, parse_mode="Markdown", reply_markup=reply_markup)
    except:
        await query.message.reply_text(menu_text, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_osint_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка введённого номера телефона"""
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_states.get(user_id) != "awaiting_phone":
        return

    if not text.startswith('+') or not text[1:].isdigit():
        await update.message.reply_text(
            "❌ *Неверный формат номера!*\n\n"
            "Номер должен начинаться с `+` и содержать только цифры\n"
            "Пример: `+79991234567`\n\n"
            "Попробуй снова или отправь /cancel",
            parse_mode="Markdown"
        )
        return

    user_states[user_id] = None

    status_msg = await update.message.reply_text(
        f"🔍 *Начинаю OSINT-поиск для* `{text}`...\n⏳ Это может занять до 30 секунд",
        parse_mode="Markdown"
    )

    try:
        result = await simple_osint_search(text)

        if result:
            cache[text] = result
            await status_msg.edit_text(
                f"📱 *Результаты OSINT для* `{text}`:\n\n{result}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")],
                    [InlineKeyboardButton("🔎 Новый поиск", callback_data="osint_search")]
                ])
            )
        else:
            await status_msg.edit_text(
                f"❌ *Не удалось найти информацию для* `{text}`\n\n"
                "💡 Убедись, что номер в международном формате",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
                ])
            )
    except Exception as e:
        await status_msg.edit_text(
            f"❌ *Ошибка:*\n`{str(e)}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
            ])
        )

async def simple_osint_search(phone_number: str) -> str:
    """Простой OSINT поиск"""
    output = []
    output.append("📊 **ИНФОРМАЦИЯ О НОМЕРЕ**")
    output.append("-" * 30)

    clean_number = phone_number.replace('+', '')
    output.append(f"📱 Номер: {phone_number}")

    # Определяем страну
    country_codes = {
        '7': 'Россия (+7)',
        '380': 'Украина (+380)',
        '375': 'Беларусь (+375)',
        '1': 'США/Канада (+1)',
        '44': 'Великобритания (+44)',
        '49': 'Германия (+49)',
        '33': 'Франция (+33)',
        '86': 'Китай (+86)',
        '91': 'Индия (+91)',
        '81': 'Япония (+81)',
        '55': 'Бразилия (+55)',
        '61': 'Австралия (+61)',
    }

    country_found = False
    for code, country in country_codes.items():
        if clean_number.startswith(code):
            output.append(f"🌍 Страна: {country}")
            country_found = True
            break

    if not country_found:
        output.append("🌍 Страна: Неизвестно")

    output.append("\n🔗 **ССЫЛКИ ДЛЯ ПОИСКА**")
    output.append("-" * 30)
    output.append(f"🔍 Google: https://www.google.com/search?q={clean_number}")
    output.append(f"🔍 DuckDuckGo: https://duckduckgo.com/?q={clean_number}")
    output.append(f"💬 WhatsApp: https://wa.me/{clean_number}")
    output.append(f"💬 Telegram: https://t.me/+{clean_number}")

    output.append("\n📌 **ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ**")
    output.append("-" * 30)
    output.append("• Truecaller: https://www.truecaller.com/search")
    output.append("• GetContact: https://getcontact.com")
    output.append("• SpyDialer: https://spydialer.com")
    output.append("• ZabaSearch: https://zabasearch.com")

    return "\n".join(output)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /ping"""
    start_time = time.time()
    await update.message.chat.send_action(action="typing")
    await asyncio.sleep(0.1)
    end_time = time.time()
    ping_ms = (end_time - start_time) * 1000

    response = (
        f"🏓 *Результат пинг-теста*\n\n"
        f"📡 Пинг: `{ping_ms:.1f} мс`\n"
        f"🕐 Время: `{datetime.now().strftime('%H:%M:%S')}`\n\n"
        f"{'🟢 Отлично!' if ping_ms < 100 else '🟡 Нормально' if ping_ms < 300 else '🔴 Медленно'}"
    )
    await update.message.reply_text(
        response,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
        ])
    )

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отмена ожидания ввода номера"""
    user_id = update.effective_user.id
    if user_id in user_states:
        user_states[user_id] = None
        await update.message.reply_text(
            "❌ *Действие отменено*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
            ])
        )
    else:
        await update.message.reply_text("🤔 Нет активных действий для отмены")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех текстовых сообщений"""
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    if user_states.get(user_id) == "awaiting_phone":
        await handle_osint_text(update, context)
    else:
        await update.message.reply_text(
            "🔍 *Используй меню для навигации*\nОтправь /start чтобы открыть главное меню",
            parse_mode="Markdown"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help"""
    help_text = (
        "📖 *Помощь по боту*\n\n"
        "🔍 *OSINT-поиск:* Нажми на кнопку и введи номер\n"
        "🏓 *Пинг:* Проверка скорости ответа бота\n"
        "ℹ️ *О боте:* Информация о версии и инструментах\n"
        "📞 *Контакты:* Связь с разработчиком\n\n"
        "❌ /cancel - Отменить ввод номера"
    )
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
        ])
    )

# ВАШИ ОБРАБОТЧИКИ КОМАНД (тут просто продолжается то, что у вас есть)
# application.add_handler(MessageHandler(...))

print("✅ Обработчики добавлены", flush=True)

# 1. Закрываем функцию main() фигурной скобкой и отступом назад
def main():
    print("🔄 Начинаем запуск бота...", flush=True)
    print("🐱 Создаём приложение...", flush=True)
    application = Application.builder().token(BOT_TOKEN).build()
    print("✅ Приложение создано", flush=True)

    print("📝 Добавляем обработчики...", flush=True)
    # ... ваши add_handler команды ...
    print("✅ Обработчики добавлены", flush=True)

    print("🤖 OSINT-бот запущен!", flush=True)
import asyncio  # Убедитесь, что эта строка есть в самом верху файла

# ... (ваши add_handler команды) ...
# ========== ЗАПУСК БОТА ==========
if name == '__main__':
    application.run_polling()

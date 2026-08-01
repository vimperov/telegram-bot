import asyncio
import time
import subprocess
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
# 👇 ВСТАВЬТЕ НОВЫЙ ТОКЕН (после сброса у BotFather)
BOT_TOKEN ="8729794388:AAHxvbqkWiSieSA9Q__KX7N-ZowXY4osIv0"
# 👇 ВСТАВЬТЕ ID КАРТИНКИ (получите у @userinfobot)
IMAGE_ID = "8102195798"
# Кэш для результатов
cache = {}
# Состояния пользователей
user_states = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветствие с красивым меню"""
    
    welcome_text = (
        "🔍 *Добро пожаловать в OSINT-Бот!*\n\n"
        "🛡️ Я помогу тебе найти информацию по номеру телефона\n"
        "📱 Использую передовые инструменты OSINT\n\n"
        "⚡ *Выбери действие ниже:*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔎 OSINT-поиск", callback_data="osint_search")],
        [InlineKeyboardButton("🏓 Проверить пинг", callback_data="ping")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if IMAGE_ID != "8102195798":
        await update.message.reply_photo(
            photo=IMAGE_ID,
            caption=welcome_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
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
            "🏓 *Измеряем пинг...*\n"
            "⏳ Пожалуйста, подожди...",
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
            "🤖 *Версия:* 2.0\n"
            "🛠️ *Инструменты:* PhoneInfoga, OSINT\n"
            "📱 *Функции:* Поиск по номеру, пинг\n\n"
            "⚡ *Сделано с ❤️ для OSINT-сообщества*"
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
            "💬 *Предложения и вопросы:*\n"
            "Всегда рад обратной связи!"
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
    menu_text = (
        "🔍 *Главное меню*\n\n"
        "🛡️ Выбери действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔎 OSINT-поиск", callback_data="osint_search")],
        [InlineKeyboardButton("🏓 Проверить пинг", callback_data="ping")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            menu_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except:
        await query.message.reply_text(
            menu_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
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
            "Номер должен начинаться с + и содержать только цифры\n"
            "Пример: `+79991234567`\n\n"
            "Попробуй снова или отправь /cancel",
            parse_mode="Markdown"
        )
        return
    
    user_states[user_id] = None
    
    status_msg = await update.message.reply_text(
        f"🔍 *Начинаю OSINT-поиск для* {text}...\n"
        "⏳ Это может занять до 30 секунд",
        parse_mode="Markdown"
    )
    
    try:
        result = await run_phoneinfoga(text)
        
        if result:
            cache[text] = result
            await status_msg.edit_text(
                f"📱 *Результаты OSINT для* {text}:\n\n{result}",
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
            f"❌ *Ошибка при выполнении поиска:*\n`{str(e)}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 В меню", callback_data="back_to_menu")]
            ])
        )
async def run_phoneinfoga(phone_number: str) -> str:
    """Запускает PhoneInfoga и возвращает результат"""
    try:
        result = subprocess.run(
            ["phoneinfoga", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except FileNotFoundError:
        return "⚠️ PhoneInfoga не установлен.\nУстановите: go install -v github.com/sundowndev/phoneinfoga/v2@latest"
    except subprocess.TimeoutExpired:
        return "⚠️ PhoneInfoga не отвечает"
    
    try:
        result = subprocess.run(
            ["phoneinfoga", "scan", "-n", phone_number, "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return f"⚠️ Ошибка выполнения: {result.stderr}"
        
        try:
            data = json.loads(result.stdout)
            return format_phoneinfoga_result(data)
        except json.JSONDecodeError:
            return "⚠️ Не удалось обработать результат"
            
    except subprocess.TimeoutExpired:
        return "⏳ Превышено время ожидания (30 сек)"
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"
def format_phoneinfoga_result(data: dict) -> str:
    """Форматирует результат PhoneInfoga"""
    output = []
    output.append("📊 **ИНФОРМАЦИЯ О НОМЕРЕ**")
    output.append("-" * 30)
    
    if "Number" in data:
        number_info = data.get("Number", {})
        output.append(f"📱 Номер: {number_info.get('RawLocal', 'Неизвестно')}")
        
        country = number_info.get('Country', {})
        if isinstance(country, dict):
            output.append(f"🌍 Страна: {country.get('Name', 'Неизвестно')}")
            output.append(f"🏷️ Код страны: {country.get('Code', 'Неизвестно')}")
        else:
            output.append(f"🌍 Страна: {country}")
        
        output.append(f"📍 Регион: {number_info.get('Region', 'Неизвестно')}")
        output.append(f"📶 Оператор: {number_info.get('Carrier', 'Неизвестно')}")
        output.append(f"📱 Тип линии: {number_info.get('LineType', 'Неизвестно')}")
    
    if "Valid" in data:
        output.append(f"✅ Валидность: {'Да' if data.get('Valid') else 'Нет'}")
    
    phone_clean = data.get('Number', {}).get('International', '').replace('+', '')
    output.append("\n🔗 **ССЫЛКИ ДЛЯ ПОИСКА**")
    output.append("-" * 30)
    output.append(f"🔍 Google: https://www.google.com/search?q={phone_clean}")
    output.append(f"🔍 DuckDuckGo: https://duckduckgo.com/?q={phone_clean}")
    output.append(f"💬 WhatsApp: https://wa.me/{phone_clean}")
    output.append(f"💬 Telegram: https://t.me/+{phone_clean}")
    
    output.append("\n📌 **ДОПОЛНИТЕЛЬНЫЕ ИНСТРУМЕНТЫ**")
    output.append("-" * 30)
    output.append("• Truecaller: https://www.truecaller.com/search")
    output.append("• GetContact: https://getcontact.com")
    
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
            "🔍 *Используй меню для навигации*\n"
            "Отправь /start чтобы открыть главное меню",
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
def main():
    """Запуск бота"""
    print("🔄 Начинаем запуск бота...", flush=True)
    
    try:
        print("📡 Создаём приложение...", flush=True)
        application = Application.builder().token(BOT_TOKEN).build()
        print("✅ Приложение создано", flush=True)
        
        print("📝 Добавляем обработчики...", flush=True)
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping_command))
        application.add_handler(CommandHandler("cancel", cancel_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        print("✅ Обработчики добавлены", flush=True)
        
        print("🔍 OSINT-бот с меню запущен!", flush=True)
        print("📌 Нажми /start в Telegram", flush=True)
        print("⏳ Нажмите Ctrl+C для остановки", flush=True)
        print("🔄 Подключаемся к Telegram...", flush=True)
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}", flush=True)
if __name__ == "__main__":
    main()
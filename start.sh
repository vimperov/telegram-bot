#!/bin/bash
echo "🚀 Запускаю бота..."
while true; do
    python bot.py
    echo "🔄 Бот упал. Ждём 30 секунд перед перезапуском..."
    sleep 30
done

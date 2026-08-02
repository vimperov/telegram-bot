#!/bin/bash
echo "Запускаю бота..."
while true; do
    python bot.py
    echo "Бот упал. Перезапуск через 30 секунд..."
    sleep 30
done

# ODOA Telegram Bot
Simple example telegram bot using [ODOA library](https://github.com/Keda87/python-quran-odoa).
This bot scheduled to send random surah & translation every day at 6:00 AM. Feel free to fork and modify this bot with your needs.

# Prerequisite:
- Python 2.7.*
- Redis

# Installation:
- Git clone [https://github.com/Keda87/odoa-telegram-bot/](https://github.com/Keda87/odoa-telegram-bot/)
- pip install -r requirements.txt

# Run:
- `$ redis-server`
- `$ celery -A tasks beat`

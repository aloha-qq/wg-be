from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = 'token'
TELEGRAM_USER_IDS = [1]

async def send_message_to_users(text: str) -> None:
    for id in TELEGRAM_USER_IDS:
        try:
            bot = Bot(token=BOT_TOKEN)
            await bot.send_message(id, text=text, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            return
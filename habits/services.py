import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str) -> None:
    if not settings.TELEGRAM_BOT_TOKEN:
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        requests.get(url, data=payload, timeout=5)
    except requests.RequestException as e:
        print(f"Error sending message: {e}")

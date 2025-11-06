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
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending message: {e}")

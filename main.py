import requests
import time
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/41"

# Memory of last known residences
previous_residences = set()

def fetch_current_residences():
    try:
        response = requests.post(API_URL)
        data = response.json()
        items = data.get("results", {}).get("items", [])
        residence_labels = set(item["residence"]["label"] for item in items if item.get("residence"))
        return residence_labels
    except Exception as e:
        print("Error fetching data:", e)
        return set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print("Message sent:", message)
    except Exception as e:
        print("Error sending message:", e)

def main_loop():
    global previous_residences
    while True:
        current_residences = fetch_current_residences()
        new_residences = current_residences - previous_residences

        if new_residences:
            for residence in new_residences:
                send_telegram_message(f"🏡 New available residence: <b>{residence}</b>")
            previous_residences = current_residences

        # Check every 2 minutes
        time.sleep(10)

if __name__ == "__main__":
    print("Bot started...")
    main_loop()

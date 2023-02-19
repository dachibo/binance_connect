import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.telegram.org/bot{}/sendMessage".format(os.environ['TG_BOT'])


def send_message_tg_bot(message: str) -> None:
    requests.post(
        url=url,
        json={"chat_id": int(os.environ['CHAT_ID_TG']), "text": message},
    )

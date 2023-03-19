import os
import requests
import gspread
import logging
from dotenv import load_dotenv

load_dotenv()


class CantGetTelegramSettings(BaseException):
    """no telegram settings received"""


class CantGetCredentials(BaseException):
    """credentials.json not found"""


def _parse_chat_id(chat_id: str):
    return int(chat_id)


def _send_message_tg_bot(message: str) -> None:
    bot_token = os.environ.get('TG_BOT')
    chat_id = os.environ.get('CHAT_ID_TG')
    if bot_token is None and chat_id is None:
        raise CantGetTelegramSettings
    requests.post(
        url=f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": _parse_chat_id(chat_id), "text": message},
    )


def _google_sheets_update(row: list):
    creds_json = os.path.dirname(__file__).replace('/src', "") + "/credentials.json"
    if os.path.exists(creds_json):
        gc = gspread.service_account(filename=creds_json)
        sheet = gc.open(title="BinanceBot")
        sheet.sheet1.append_row(row)
    else:
        raise CantGetCredentials


def send_messages(message_to_tg: str, message_to_google: list):
    try:
        _send_message_tg_bot(message=message_to_tg)
        _google_sheets_update(row=message_to_google)
    except CantGetTelegramSettings as e:
        logging.error(e)
    except CantGetCredentials as e:
        logging.error(e)

import os
import certifi
import logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from candlestick_finder import CandlestickFinder
from models import parse_realtime_kline, parse_historical_klines, Kline
from send_messages import send_messages

logging.basicConfig(
    filename="logs.log",
    level="DEBUG",
    format="%(name)s | %(asctime)s | %(message)s")

client = UMFutures()


def check_patterns(historical_klines: list[Kline], symbol: str, interval: str):
    finder = CandlestickFinder(data=historical_klines)
    message_to_tg = message_to_google = None
    if finder.is_railway_pattern():
        message_to_tg = f"Рельсы на {symbol}"
        message_to_google = ["Рельсы", symbol, interval, int(finder.current_bar.CloseTime)]
    elif finder.is_pin_bar_pattern():
        message_to_tg = f"Пин-бар на {symbol}"
        message_to_google = ["Пин-бар", symbol, interval, int(finder.current_bar.CloseTime)]
    return message_to_tg, message_to_google


def main(msg):
    if 'result' not in msg and msg['k']['x'] is True:
        kline = parse_realtime_kline(message=msg)
        symbol, interval = kline['symbol'], kline['interval']
        message_historical = client.klines(symbol=symbol, interval=interval, limit=14)[:-1]
        historical_klines = parse_historical_klines(symbol=symbol, interval=interval, message=message_historical)
        historical_klines.append(kline)
        message_to_tg, message_to_google = check_patterns(historical_klines=historical_klines, symbol=symbol,
                                                          interval=interval)
        if message_to_tg is not None and message_to_google is not None:
            send_messages(message_to_tg=message_to_tg, message_to_google=message_to_google)


if __name__ == '__main__':
    os.environ['SSL_CERT_FILE'] = certifi.where()
    my_client = UMFuturesWebsocketClient()
    my_client.start()
    my_client.kline(symbol="BTCUSDT", id=1, interval="1m", callback=main)
    # my_client.kline(symbol="BTCUSDT", id=1, interval="1h", callback=main)
    # win32api.SetConsoleCtrlHandler(lambda _: ws_client.stop(), True)

import os
import certifi
import pandas as pd
import logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from binance.um_futures import UMFutures
from candlestick_finder import CandlestickFinder
from dataframe_handlers import create_frame_realtime, create_frame_historical
from tg_bot import send_message_tg_bot
from google_sheets import google_sheets_update


logging.basicConfig(
    filename="logs.log",
    level="DEBUG",
    format="%(name)s | %(asctime)s | %(message)s")

client = UMFutures()


def check_patterns(symbol, df, interval):
    finder = CandlestickFinder(df)
    if finder.is_railway_pattern():
        send_message_tg_bot(f"Рельсы на {symbol}")
        google_sheets_update(["Рельсы", symbol, interval, int(finder.current_bar.CloseTime)])
    elif finder.is_pin_bar_pattern():
        send_message_tg_bot(f"Пин-бар на {symbol}")
        google_sheets_update(["Пин-бар", symbol, interval, int(finder.current_bar.CloseTime)])


def main(msg):
    if 'result' not in msg and msg['k']['x'] is True:
        symbol, kline, interval = msg['s'], msg['k'], msg['k']['i']
        logging.info(symbol, kline, interval)
        df_realtime = create_frame_realtime(kline)
        klines = client.klines(symbol=symbol, interval=interval, limit=14)[:-1]
        df_historical = create_frame_historical(klines=klines)
        all_df = pd.concat([df_realtime, df_historical])
        check_patterns(symbol=symbol, df=all_df, interval=interval)


if __name__ == '__main__':
    os.environ['SSL_CERT_FILE'] = certifi.where()
    my_client = UMFuturesWebsocketClient()
    my_client.start()
    my_client.kline(symbol="BTCUSDT", id=1, interval="30m", callback=main)
    my_client.kline(symbol="BTCUSDT", id=1, interval="1h", callback=main)
    # win32api.SetConsoleCtrlHandler(lambda _: ws_client.stop(), True)

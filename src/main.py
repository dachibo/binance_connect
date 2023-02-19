import os
import certifi
import pandas as pd
import numpy as np
import logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from dotenv import load_dotenv
from patterns import rails
from tg_bot import send_message_tg_bot

logging.basicConfig(
    filename="logs.log",
    level="DEBUG",
    format="%(name)s | %(asctime)s | %(message)s")

load_dotenv()
um_futures_client = UMFutures(key=os.environ["API_KEY"], secret=os.environ["SECRET_KEY"])


def rename_and_astype(df):
    df.columns = ["OpenTime", "Open", "High", "Low", "Close", "Volume"]
    df[["Open", "High", "Low", "Close", "Volume"]] = df[
        ["Open", "High", "Low", "Close", "Volume"]].astype(float)
    df.OpenTime = pd.to_datetime(df.OpenTime, unit='ms')
    df["Average"] = np.where(df.Close > df.Open, df.Close - df.Open, df.Open - df.Close)
    return df


def create_frame_historical(klines):
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1, 2, 3, 4, 5]]
    df = rename_and_astype(df)
    return df.sort_values(by="OpenTime", ascending=False)


def create_frame_realtime(kline):
    df = pd.DataFrame([kline])
    df = df.loc[:, ['t', 'o', 'h', 'l', 'c', 'v']]
    df = rename_and_astype(df)
    return df


def check_patterns(symbol, df, average=None):
    rail = rails(df_first_bar=df.iloc[0], df_second_bar=df.iloc[1],
                 total_average=average)
    if rail:
        send_message_tg_bot(f"Рельсы на {symbol}")


def main(msg):
    if 'result' not in msg and msg['k']['x'] is True:
        symbol, kline, interval = msg['s'], msg['k'], msg['k']['i']
        df_realtime = create_frame_realtime(kline)
        klines = um_futures_client.klines(symbol=symbol, interval=interval, limit=5)[:-1]
        df_historical = create_frame_historical(klines=klines)
        all_df = pd.concat([df_realtime, df_historical])
        logging.info(all_df)
        check_patterns(symbol=symbol,
                       df=all_df,
                       average=round(df_historical.Average.mean(), 2))


if __name__ == '__main__':
    os.environ['SSL_CERT_FILE'] = certifi.where()
    my_client = UMFuturesWebsocketClient()
    my_client.start()
    my_client.kline(symbol="BTCUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="ETHUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="XRPUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="EOSUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="LTCUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="TRXUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="ETCUSDT", id=1, interval="1h", callback=main)
    my_client.kline(symbol="ADAUSDT", id=1, interval="1h", callback=main)
    # win32api.SetConsoleCtrlHandler(lambda _: ws_client.stop(), True)

import os, certifi
from dotenv import load_dotenv
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
import pandas as pd
import numpy as np
from patterns import rails, pinbar

# TODO раздобыть отработанные паттерны, написать тесты, замокать `um_futures_client.klines`


load_dotenv()
um_futures_client = UMFutures(key=os.environ["API_KEY"], secret=os.environ["SECRET_KEY"])


def get_historical(symbol: str, interval: str = "30m", limit: int = 10):
    df = pd.DataFrame(um_futures_client.klines(symbol=symbol, interval=interval, limit=limit))
    df = df.loc[:, [0, 1, 2, 3, 4, 5]]
    df.columns = ["OpenTime", "Open", "High", "Low", "Close", "Volume"]
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].astype(float)
    df.OpenTime = pd.to_datetime(df.OpenTime, unit='ms')
    df["Average"] = np.where(df.Close > df.Open, df.Close - df.Open, df.Open - df.Close)
    return df.sort_values(by="OpenTime", ascending=False)


def create_frame_realtime(msg):
    msg.update(msg.pop('k'))
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'i', 'o', 'c']]
    df.columns = ['symbol', 'time', 'interval', 'open', 'close']
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.time = pd.to_datetime(df.time, unit='ms')
    return df


def check_patterns(df, average=None):
    rails(df_first_bar=df.iloc[0], df_second_bar=df.iloc[1], total_average=average)


def main(msg):
    if 'result' not in msg and msg['k']['x'] is True:
        df_realtime = create_frame_realtime(msg)
        df_historical = get_historical(symbol=df_realtime.symbol[0], interval=df_realtime.interval[0])
        check_patterns(df_historical, average=round(df_historical.Average.mean(), 2))


if __name__ == '__main__':
    os.environ['SSL_CERT_FILE'] = certifi.where()
    my_client = UMFuturesWebsocketClient()
    my_client.start()
    my_client.kline(symbol="BTCUSDT", id=1, interval="5m", callback=main)
    # win32api.SetConsoleCtrlHandler(lambda _: ws_client.stop(), True)

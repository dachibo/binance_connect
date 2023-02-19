import pandas as pd
import numpy as np


def rename_and_astype(df: pd.DataFrame):
    df.columns = ["OpenTime", "Open", "High", "Low", "Close", "Volume"]
    df[["Open", "High", "Low", "Close", "Volume"]] = df[
        ["Open", "High", "Low", "Close", "Volume"]].astype(float)
    df.OpenTime = pd.to_datetime(df.OpenTime, unit='ms')
    df["Average"] = np.where(df.Close > df.Open, df.Close - df.Open, df.Open - df.Close)
    df["Direction"] = np.where(df.Close > df.Open, "long", "short")
    return df


def create_frame_historical(klines: list):
    df = pd.DataFrame(klines)
    df = df.loc[:, [0, 1, 2, 3, 4, 5]]
    df = rename_and_astype(df)
    return df.sort_values(by="OpenTime", ascending=False)


def create_frame_realtime(kline: dict):
    df = pd.DataFrame([kline])
    df = df.loc[:, ['t', 'o', 'h', 'l', 'c', 'v']]
    df = rename_and_astype(df)
    return df

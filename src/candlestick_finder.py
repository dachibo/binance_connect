import pandas as pd
import numpy as np
from src.models import Kline


def create_frame_historical(klines: list[Kline]) -> pd.DataFrame:
    df = pd.DataFrame(klines)
    df["average"] = np.where(df.close > df.open_price, df.close - df.open_price, df.open_price - df.close)
    df["direction"] = np.where(df.close > df.open_price, "long", "short")
    return df


class CandlestickFinder:
    def __init__(self, data: list[Kline]):
        self.data = create_frame_historical(klines=data)
        self.current_bar = self.data.iloc[-1]
        self.prev_bar = self.data.iloc[-2]

    def atr(self, n=14):
        high_low = self.data['high'] - self.data['low']
        high_close = np.abs(self.data['high'] - self.data['close'].shift())
        low_close = np.abs(self.data['low'] - self.data['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(n).sum().values[-1] / n

    def is_railway_pattern(self) -> bool:
        if self.current_bar.direction != self.prev_bar.direction:
            if self.current_bar.average > self.atr() < self.prev_bar.average:
                percent = (self.current_bar.close - self.prev_bar.open_price) / self.current_bar.open_price * 100
                return float(-0.1) < percent < float(0.5)
            return False
        return False

    def is_pin_bar_pattern(self) -> bool:
        realbody = abs(self.current_bar.open_price - self.current_bar.close)
        candle_range = self.current_bar.high - self.current_bar.low

        if candle_range > self.atr():
            return (realbody <= candle_range / 3 and min(self.current_bar.open_price, self.current_bar.close) > (
                    self.current_bar.high + self.current_bar.low) / 2 and self.current_bar.low < self.prev_bar.low) or \
                   (realbody <= candle_range / 3 and max(self.current_bar.open_price, self.current_bar.close) < (
                           self.current_bar.high + self.current_bar.low) / 2 and self.current_bar.high > self.prev_bar.high)
        return False

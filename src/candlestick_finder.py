import pandas as pd
import numpy as np


class CandlestickFinder:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.current_bar = data.iloc[0]
        self.prev_bar = data.iloc[1]

    def atr(self, n=14):
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(n).sum().values[-1] / n

    def is_railway_pattern(self) -> bool:
        if self.current_bar.Direction != self.prev_bar.Direction:
            if self.current_bar.Average > self.atr() < self.prev_bar.Average:
                percent = (self.current_bar.Close - self.prev_bar.Open) / self.current_bar.Open * 100
                return float(-0.1) < percent < float(0.5)
            return False
        return False

    def is_pin_bar_pattern(self) -> bool:
        realbody = abs(self.current_bar.Open - self.current_bar.Close)
        candle_range = self.current_bar.High - self.current_bar.Low

        if candle_range > self.atr():
            return (realbody <= candle_range / 3 and min(self.current_bar.Open, self.current_bar.Close) > (
                            self.current_bar.High + self.current_bar.Low) / 2 and self.current_bar.Low < self.prev_bar.Low) or \
                (realbody <= candle_range / 3 and max(self.current_bar.Open, self.current_bar.Close) < (
                         self.current_bar.High + self.current_bar.Low) / 2 and self.current_bar.High > self.prev_bar.High)
        return False

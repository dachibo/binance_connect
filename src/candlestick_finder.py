import pandas as pd


class CandlestickFinder:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.current_bar = data.iloc[0]
        self.prev_bar = data.iloc[1]

    def is_railway_pattern(self) -> bool:
        bar_size_medium = self.data[2:].Average.mean()

        if self.current_bar.Direction != self.prev_bar.Direction:
            if self.current_bar.Average > (bar_size_medium * 1.2) < self.prev_bar.Average:
                percent = (self.current_bar.Close - self.prev_bar.Open) / self.current_bar.Open * 100
                return float(-0.1) < percent < float(0.5)
            return False
        return False

    def is_pin_bar_pattern(self) -> bool:
        bar_size_medium = self.data[1:].Average.mean()
        realbody = abs(self.current_bar.Open - self.current_bar.Close)
        candle_range = self.current_bar.High - self.current_bar.Low

        if self.current_bar.Average > (bar_size_medium * 1.2):
            return (realbody <= candle_range / 3 and min(self.current_bar.Open, self.current_bar.Close) > (
                self.current_bar.High + self.current_bar.Low) / 2 and self.current_bar.Low < self.prev_bar.Low) or \
               (realbody <= candle_range / 3 and max(self.current_bar.Open, self.current_bar.Close) < (
                       self.current_bar.High + self.current_bar.Low) / 2 and self.current_bar.High > self.prev_bar.High)
        return False

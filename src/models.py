from typing import TypedDict, List
from datetime import datetime


class Kline(TypedDict):
    symbol: str
    interval: str
    close_time: datetime
    open_price: float
    high: float
    low: float
    close: float
    volume: float


def parse_realtime_kline(message: dict) -> Kline:
    return Kline(
        symbol=message['s'],
        interval=message['k']['i'],
        close_time=datetime.fromtimestamp(message['k']['T'] / 1000.0),
        open_price=float(message['k']['o']),
        high=float(message['k']['h']),
        low=float(message['k']['l']),
        close=float(message['k']['c']),
        volume=float(message['k']['v'])
    )


def parse_historical_klines(symbol: str, interval: str, message: list[list]) -> List[Kline]:
    return [Kline(
        symbol=symbol,
        interval=interval,
        close_time=datetime.fromtimestamp(kl[6] / 1000.0),
        open_price=float(kl[1]),
        high=float(kl[2]),
        low=float(kl[3]),
        close=float(kl[4]),
        volume=float(kl[5])
    ) for kl in message]

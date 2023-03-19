from src import CandlestickFinder
from src.models import parse_historical_klines, parse_realtime_kline, Kline
from datetime import datetime


def test_parse_realtime_kline():
    message = {
        "e": "kline",
        "E": 1638747660000,
        "s": "BTCUSDT",
        "k": {
            "t": 1638747660000,
            "T": 1638747719999,
            "s": "BTCUSDT",
            "i": "1m",
            "f": 100,
            "L": 200,
            "o": "0.0010",
            "c": "0.0020",
            "h": "0.0025",
            "l": "0.0015",
            "v": "1000",
            "n": 100,
            "x": False,
            "q": "1.0000",
            "V": "500",
            "Q": "0.500",
            "B": "123456"
        }
    }
    kline = parse_realtime_kline(message=message)
    assert kline['symbol'] == message['s']
    assert kline['interval'] == message['k']['i']
    assert kline['close_time'] == datetime.fromtimestamp(message['k']['T'] / 1000.0)
    assert kline['open_price'] == float(message['k']['o'])
    assert kline['high'] == float(message['k']['h'])
    assert kline['low'] == float(message['k']['l'])
    assert kline['close'] == float(message['k']['c'])
    assert kline['volume'] == float(message['k']['v'])


def test_patterns(history_klines):
    for pattern, klines in history_klines.items():
        for kline in klines:
            df = parse_historical_klines(symbol="", interval="", message=kline)
            finder = CandlestickFinder(data=df)
            if pattern == 'rails':
                assert finder.is_railway_pattern()
            elif pattern == 'pinbars':
                assert finder.is_pin_bar_pattern()


def test_not_patterns(history_bad_klines):
    for pattern, klines in history_bad_klines.items():
        for kline in klines:
            df = parse_historical_klines(symbol="", interval="", message=kline)
            finder = CandlestickFinder(data=df)
            if pattern == 'rails':
                assert not finder.is_railway_pattern()
            elif pattern == 'pinbars':
                assert not finder.is_pin_bar_pattern()

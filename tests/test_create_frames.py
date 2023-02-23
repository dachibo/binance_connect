from src import create_frame_realtime, create_frame_historical


realtime_kline = {
    "t": 1638747660000,  # Kline start time
    "T": 1638747719999,  # Kline close time
    "s": "BTCUSDT",  # Symbol
    "i": "1m",  # Interval
    "f": 100,  # First trade ID
    "L": 200,  # Last trade ID
    "o": "0.0010",  # Open price
    "c": "0.0020",  # Close price
    "h": "0.0025",  # High price
    "l": "0.0015",  # Low price
    "v": "1000",  # Base asset volume
    "n": 100,  # Number of trades
    "x": False,  # Is this kline closed?
    "q": "1.0000",  # Quote asset volume
    "V": "500",  # Taker buy base asset volume
    "Q": "0.500",  # Taker buy quote asset volume
    "B": "123456"  # Ignore
}

klines_historical = [
    [
        1499040000000,  # Open time
        "0.01634790",  # Open
        "0.80000000",  # High
        "0.01575800",  # Low
        "0.01577100",  # Close
        "148976.11427815",  # Volume
        1499644799999,  # Close time
        "2434.19055334",  # Quote asset volume
        308,  # Number of trades
        "1756.87402397",  # Taker buy base asset volume
        "28.46694368",  # Taker buy quote asset volume
        "17928899.62484339"  # Ignore.
    ]
]


def test_create_frame_realtime():
    fr = create_frame_realtime(realtime_kline)
    assert fr.Open[0] == float(realtime_kline["o"])
    assert fr.High[0] == float(realtime_kline["h"])
    assert fr.Low[0] == float(realtime_kline["l"])
    assert fr.Close[0] == float(realtime_kline["c"])
    assert fr.Volume[0] == float(realtime_kline["v"])
    assert fr.CloseTime[0] == realtime_kline["T"]
    assert "Average" in fr.columns
    assert fr.Direction[0] in ("long", "short")


def test_create_frame_historical():
    fr = create_frame_historical(klines_historical)
    assert fr.Open[0] == float(klines_historical[0][1])
    assert fr.High[0] == float(klines_historical[0][2])
    assert fr.Low[0] == float(klines_historical[0][3])
    assert fr.Close[0] == float(klines_historical[0][4])
    assert fr.Volume[0] == float(klines_historical[0][5])
    assert fr.CloseTime[0] == klines_historical[0][6]
    assert "Average" in fr.columns
    assert fr.Direction[0] in ("long", "short")

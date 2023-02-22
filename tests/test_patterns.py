from src.dataframe_handlers import create_frame_historical
from src.candlestick_finder import CandlestickFinder
from src.main import check_patterns


def test_rails(history_klines):
    for rail in history_klines['rails']:
        df = create_frame_historical(klines=rail)
        assert CandlestickFinder(data=df).is_railway_pattern()


def test_pinbar(history_klines):
    for pin in history_klines['pinbars']:
        df = create_frame_historical(klines=pin)
        assert CandlestickFinder(data=df).is_pin_bar_pattern()


def test_create_txt_file(history_klines):
    for pattern, history in history_klines.items():
        for klines in history:
            df = create_frame_historical(klines=klines)
            check_patterns(symbol='test', df=df)
from src import create_frame_historical, CandlestickFinder


def test_rails(history_klines):
    for rail in history_klines['rails']:
        df = create_frame_historical(klines=rail)
        assert CandlestickFinder(data=df).is_railway_pattern()


def test_not_rails(history_bad_klines):
    for rail in history_bad_klines['rails']:
        df = create_frame_historical(klines=rail)
        assert not CandlestickFinder(data=df).is_railway_pattern()


def test_pinbar(history_klines):
    for pin in history_klines['pinbars']:
        df = create_frame_historical(klines=pin)
        assert CandlestickFinder(data=df).is_pin_bar_pattern()


def test_not_pinbar(history_bad_klines):
    for pin in history_bad_klines['pinbars']:
        df = create_frame_historical(klines=pin)
        assert not CandlestickFinder(data=df).is_pin_bar_pattern()

# def test_create_txt_file(history_klines):
#     for pattern, history in history_klines.items():
#         for klines in history:
#             df = create_frame_historical(klines=klines)
#             check_patterns(symbol='test', df=df)

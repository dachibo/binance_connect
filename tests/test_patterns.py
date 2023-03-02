from src import create_frame_historical, CandlestickFinder


def test_patterns(history_klines):
    for pattern, klines in history_klines.items():
        for kline in klines:
            df = create_frame_historical(klines=kline)
            finder = CandlestickFinder(data=df)
            if pattern == 'rails':
                assert finder.is_railway_pattern()
            elif pattern == 'pinbars':
                assert finder.is_pin_bar_pattern()


def test_not_patterns(history_bad_klines):
    for pattern, klines in history_bad_klines.items():
        for kline in klines:
            df = create_frame_historical(klines=kline)
            finder = CandlestickFinder(data=df)
            if pattern == 'rails':
                assert not finder.is_railway_pattern()
            elif pattern == 'pinbars':
                assert not finder.is_pin_bar_pattern()


# def test_create_txt_file(history_klines):
#     for pattern, history in history_klines.items():
#         for klines in history:
#             df = create_frame_historical(klines=klines)
#             check_patterns(symbol='test', df=df)

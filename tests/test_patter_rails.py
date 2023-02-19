from src.main import create_frame_historical
from patterns import rails


def test_good_rails(history_klines):
    for rail in history_klines['rails']:
        df = create_frame_historical(klines=rail)
        result_rails = rails(df_first_bar=df.iloc[0], df_second_bar=df.iloc[1],
                             total_average=round(df.Average.mean(), 2))
        assert result_rails

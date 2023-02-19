def rails(df_first_bar, df_second_bar, total_average: float) -> bool:
    """

    :param total_average:
    :param df_second_bar:
    :param df_first_bar:
    :return:
    """
    price_direction_first_bar = "long" if df_first_bar.Open < df_first_bar.Close else "short"
    price_direction_second_bar = "long" if df_second_bar.Open < df_second_bar.Close else "short"

    if price_direction_first_bar != price_direction_second_bar:
        if df_first_bar.Average > (total_average * 1.2) < df_second_bar.Average:
            percent = (df_first_bar.Close - df_second_bar.Open) / df_second_bar.Open * 100
            return float(-0.1) < percent < float(0.5)
        return False
    return False

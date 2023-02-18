
def rails(df_first_bar, df_second_bar, total_average):
    """

    :param total_average:
    :param df_second_bar:
    :param df_first_bar:
    :return:
    """
    if df_first_bar.Average > (total_average*1.5) < df_second_bar.Average:
        percent = (df_first_bar.Close - df_second_bar.Open) / df_second_bar.Open * 100
        print(df_first_bar.OpenTime)
        return float(-0.1) < percent < float(0.1)


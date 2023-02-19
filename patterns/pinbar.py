def pinbar(current_bar, prev_bar, total_average: float) -> bool:
    """

    :param total_average:
    :param prev_bar:
    :param current_bar:
    :return:
    """
    return (current_bar.Average <= total_average / 3 and min(current_bar.Open, current_bar.Close) >
            (current_bar.High + current_bar.Low) / 2 and current_bar.Low < prev_bar.Low) or \
        (current_bar.Average <= total_average / 3 and min(current_bar.Open, current_bar.Close) <
         (current_bar.High + current_bar.Low) / 2 and current_bar.Low < prev_bar.Low)

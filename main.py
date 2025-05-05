import matplotlib.pyplot as plt
import pandas as pd

import src.match as m
import src.utils as utl
from statsbombpy import sb


def display_shots():
    utl.print_competition_info(55, 282)
    utl.print_events_info(3938637)
    m.display_shots(3938637)
    # print_competition_bayer()
    # df = competition_df(9, 281)
    # print(df)
    plt.show()


def print_euro_matches():
    print(sb.matches(55, 282))


def print_events():
    match_df = sb.events(3938637)
    # print(match_df.drop(4).head(10))
    print(match_df.shape)
    print(len(match_df.columns))
    match_df_nonflat = sb.events(3938637, flatten_attrs=False)
    # print(match_df.drop(4).head(10))
    print(match_df_nonflat.shape)
    print(len(match_df_nonflat.columns))
    main_set = set(match_df.columns.to_list())
    print(f"Flatten set: {main_set}")
    non_flat_set = set(match_df_nonflat.columns.to_list())
    print(f"Normal set: {non_flat_set}")
    print("Dzilania: ")
    union = main_set.union(non_flat_set)
    print(union)
    print(len(union))
    intersection = main_set.issubset(non_flat_set)
    print(intersection)
    print(match_df_nonflat.drop(6).head(10)['type'])


if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # print(len(PLURALS))
    # print(PLURALS)

    display_shots()

    # turkey_match_id = 3942382
    # dennmark_match_id = 3930171
    # belgium_match_id = 3941019
    # switzerland_match_id = 3940878

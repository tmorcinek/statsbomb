import matplotlib.pyplot as plt
from statsbombpy import sb
import pandas as pd
import utils as utl
import match as m


def display_shots():
    json = '../open-data/data/events/3938637.json'
    # utl.display_shots(json)
    # print_events(json)
    # utl.print_competitions()
    # utl.print_competition(55, 282)
    utl.print_match(3938637)
    # m.print_match(3938637)
    m.display_shots(json)
    # print_competition_bayer()
    # df = competition_df(9, 281)
    # print(df)
    plt.show()


def print_competitions():
    competitions = sb.competitions()
    filtered_competitions = competitions[(competitions['match_available_360'].notnull()) & (competitions['competition_international'] == True)]
    print(filtered_competitions)


def print_spanish_matches():
    matches = sb.matches(55, 282)
    team_name = 'Spain'
    matches_spain = matches[(matches['home_team'] == team_name) | (matches['away_team'] == team_name)]
    print(matches_spain)


if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # display_shots()
    # print_competitions()

    # print_spanish_matches()
    lineups = sb.lineups(3943043)
    # # players  = lineups[lineups['country'] == 'Spain']
    print(lineups)

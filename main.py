import matplotlib.pyplot as plt
import pandas as pd

import match as m
import utils as utl
import src.lineups.pitch as pt
import src.lineups.lineups as ln
from statsbombpy import sb


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


def display_competition_lineups():
    matches = sb.matches(55, 282)
    for _, match in matches.iterrows():
        match_id = match['match_id']
        pt.display_starting_lineups(match_id)
        positions = ln.starting_lineups(match_id)
        for key, value in positions.items():
            pt.display_starting_lineup(key, value)


if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    display_shots()
    # print_competitions()
    # print_spanish_matches()
    # display_competition_lineups()
    # print(matches)
    #
    #
    # turkey_match_id = 3942382
    # dennmark_match_id = 3930171
    # belgium_match_id = 3941019
    # switzerland_match_id = 3940878


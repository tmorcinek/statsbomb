import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch

import src.match as m
import utils as utl
from src.frames import plot_polygon, plot_frame_group
from src.matches import display_competition_lineups
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


def print_euro_matches():
    matches = sb.matches(55, 282)
    print(matches)

def print_spanish_matches():
    matches = sb.matches(55, 282)
    team_name = 'Spain'
    matches_spain = matches[(matches['home_team'] == team_name) | (matches['away_team'] == team_name)]
    print(matches_spain)




if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # match = sb.events(3938637)
    # print(match)
    frames = sb.frames(3938637)
    grouped = frames.groupby('id')
    for group_id, group_df in grouped:
        pitch = Pitch(pitch_type='statsbomb')
        fig, ax = pitch.draw(figsize=(10, 7))
        print(group_df)
        plot_polygon(group_df.iloc[0]['visible_area'], pitch, ax)
        plot_frame_group(group_df, pitch, ax)
        plt.show()
        # print(f"Group: {group_id}")

    # display_shots()
    # print_euro_matches()
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


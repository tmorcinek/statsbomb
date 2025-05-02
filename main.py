import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import VerticalPitch, Pitch

import match as m
import utils as utl
from statsbombpy import sb
import src.lineups as ln
import src.pitch as pt


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


def display_players_formation(players):
    # przykładowe rozmieszczenie pozycji (4-3-3)
    formation_coords = [
        (5, 5), (25, 5), (45, 5), (65, 5),  # obrońcy
        (25, 30), (45, 30), (65, 30),  # pomocnicy
        (15, 50), (35, 55), (55, 50)  # napastnicy
    ]
    players_outfield = players[players['position_name'] != 'Goalkeeper'].head(10)
    gk = players[players['position_name'] == 'Goalkeeper'].head(1)
    # przygotuj DataFrame z pozycjami
    df = players_outfield.copy().reset_index(drop=True)
    df['x'], df['y'] = zip(*formation_coords)
    pitch = VerticalPitch(pitch_type='statsbomb', half=True, goal_type='box')
    fig, ax = pitch.draw(figsize=(8, 6))
    # zawodnicy z pola
    pitch.scatter(df['x'], df['y'], s=500, color='royalblue', ax=ax)
    for i, row in df.iterrows():
        pitch.annotate(row['player_name'], (row['x'], row['y'] + 1), ax=ax,
                       ha='center', va='bottom', fontsize=10, color='white')
    # bramkarz
    if not gk.empty:
        pitch.scatter(35, 1, s=500, color='green', ax=ax)
        pitch.annotate(gk.iloc[0]['player_name'], (35, 2), ax=ax,
                       ha='center', va='bottom', fontsize=10, color='white')
    plt.title(f"Spain Starting XI")
    plt.show()


def display_formation():
    # Tworzenie boiska
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 7))
    # Definicja pozycji dla formacji 4-3-3
    positions = {
        'Goalkeeper': (5, 40),
        'Right Back': (20, 10),
        'Right Center Back': (20, 30),
        'Left Center Back': (20, 50),
        'Left Back': (20, 70),
        'Right Midfield': (50, 20),
        'Center Midfield': (50, 40),
        'Left Midfield': (50, 60),
        'Right Wing': (80, 10),
        'Center Forward': (80, 40),
        'Left Wing': (80, 70)
    }
    # Rysowanie zawodników na boisku
    for position, (x, y) in positions.items():
        pitch.scatter(x, y, s=300, ax=ax)
        pitch.annotate(position, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')
    plt.title('Formacja 4-3-3')
    plt.show()


def display_vert_half_formation():
    # Tworzenie połowy pionowego boiska
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
    fig, ax = pitch.draw(figsize=(6, 8))  # Dostosuj rozmiar figury według potrzeb

    # Definicja pozycji dla formacji 4-3-3 na połowie boiska
    positions = {
        'Goalkeeper': (5, 40),
        'Right Back': (20, 10),
        'Right Center Back': (20, 30),
        'Left Center Back': (20, 50),
        'Left Back': (20, 70),
        'Right Midfield': (50, 20),
        'Center Midfield': (50, 40),
        'Left Midfield': (50, 60),
        'Right Wing': (80, 10),
        'Center Forward': (80, 40),
        'Left Wing': (80, 70)
    }

    # Rysowanie zawodników na boisku
    for position, (x, y) in positions.items():
        pitch.scatter(x, y, s=300, ax=ax)
        pitch.annotate(position, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')

    plt.title('Formacja 4-3-3')
    plt.show()


def display_vert_formation(starting_players):
    # Definicja współrzędnych dla przykładowej formacji 4-3-3
    position_coords = {
        'Goalkeeper': (5, 40),
        'Right Back': (20, 10),
        'Right Center Back': (20, 30),
        'Left Center Back': (20, 50),
        'Left Back': (20, 70),
        'Right Midfield': (50, 20),
        'Center Midfield': (50, 40),
        'Left Midfield': (50, 60),
        'Right Wing': (80, 10),
        'Center Forward': (80, 40),
        'Left Wing': (80, 70)
    }

    # Przypisanie współrzędnych do zawodników
    starting_players['x'] = starting_players['starting_position'].apply(
        lambda pos: position_coords.get(pos, (0, 0))[0]
    )
    starting_players['y'] = starting_players['starting_position'].apply(
        lambda pos: position_coords.get(pos, (0, 0))[1]
    )

    # Rysowanie boiska i zawodników
    pitch = VerticalPitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(8, 6))

    # Rysowanie zawodników
    pitch.scatter(starting_players['x'], starting_players['y'], s=500, color='royalblue', ax=ax)
    for _, row in starting_players.iterrows():
        pitch.annotate(row['player_name'], (row['x'], row['y'] + 1), ax=ax,
                       ha='center', va='bottom', fontsize=10, color='white')

    plt.title(f" Starting XI")
    plt.show()




if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # display_shots()
    # print_competitions()
    # print_spanish_matches()
    # matches = sb.matches(55, 282)
    # for _, match in matches.iterrows():
    #     print(match)
    #     match_id = match['match_id']
    #     positions = ln.starting_lineups(match_id)
    #     for key, value in positions.items():
    #         pt.display_starting_lineup(key, value)
    # # print(matches)
    #
    #
    # turkey_match_id = 3942382
    # dennmark_match_id = 3930171
    # belgium_match_id = 3941019
    # switzerland_match_id = 3940878


    positions = ln.starting_lineups(3943043)
    # print(positions)
    pt.display_starting_lineups(positions)

    # england_ = positions['Spain']
    # print(england_)
    # pt.display_starting_lineup('Netherlands', england_)

    # print(len(positions))

    # ln_unique_positions = ln.unique_positions(3943043)
    # print(ln_unique_positions)
    # print(len(ln_unique_positions))


    # display_players_formation(players)

    # display_vert_half_formation()
    # display_vert_half_formation()

    # pt.display_half_pitch()

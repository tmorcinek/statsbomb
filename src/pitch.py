from functools import partial

import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import VerticalPitch


def __get_position_coordinates(position_name):
    positions = {
        # Goalkeeper
        'Goalkeeper': (8, 40),

        # Defenders
        'Left Back': (20, 10),
        'Left Center Back': (20, 30),
        'Center Back': (20, 40),
        'Right Center Back': (20, 50),
        'Right Back': (20, 70),

        # Defensive Midfield
        'Left Wing Back': (30, 5),
        'Left Defensive Midfield': (30, 25),
        'Center Defensive Midfield': (30, 40),
        'Right Defensive Midfield': (30, 55),
        'Right Wing Back': (30, 75),

        # Midfield
        'Left Midfield': (40, 20),
        'Left Center Midfield': (40, 30),
        'Right Center Midfield': (40, 50),
        'Right Midfield': (40, 60),

        # Attacking Midfield
        'Left Attacking Midfield': (45, 30),
        'Center Attacking Midfield': (45, 40),
        'Right Attacking Midfield': (45, 50),

        # Forwards
        'Left Wing': (55, 10),
        'Left Center Forward': (55, 30),
        'Center Forward': (55, 40),
        'Right Center Forward': (55, 50),
        'Right Wing': (55, 70)
    }

    return positions.get(position_name, None)


def __coordinates(position_name, mirror=False, pitch_length=120, pitch_width=80):
    print(f'__coordinates: {position_name} {mirror}')
    x, y = __get_position_coordinates(position_name)
    if mirror:
        return pitch_length - x, pitch_width - y
    else:
        return x, y


def __scatter_lineup(ax, pitch, lineup, color, coordinates_func):
    for _, player in lineup.iterrows():
        x, y = coordinates_func(player['starting_position'])
        display_name = player['player_nickname'] if pd.notnull(player['player_nickname']) else player['player_name']

        pitch.scatter(x, y, s=300, ax=ax, color=color)
        pitch.annotate(display_name, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')


def __index_color(index) -> str:
    if index % 2 == 0:
        return 'royalblue'
    else:
        return 'red'


def display_starting_lineup(team_name, lineup):
    pitch = VerticalPitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(6, 8))

    ax.set_ylim(-1, 60)

    for _, player in lineup.iterrows():
        x, y = __coordinates(player['starting_position'])
        display_name = player['player_nickname'] if pd.notnull(player['player_nickname']) else player['player_name']

        pitch.scatter(x, y, s=300, ax=ax, color='royalblue')
        pitch.annotate(display_name, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')

    plt.title(f'{team_name} Starting XI')
    plt.show()


def display_starting_lineups(lineups):
    pitch = VerticalPitch(pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(6, 8))

    index = 0
    for key, value in lineups.items():
        partial_coordinates = partial(__coordinates, mirror=True if index == 0 else False)
        __scatter_lineup(ax, pitch, value, __index_color(index), partial_coordinates)
        index += 1

    plt.title(f'Starting XI')
    plt.show()

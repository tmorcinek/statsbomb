import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import VerticalPitch, Pitch


def _get_position_coordinates(position_name):
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


def display_starting_lineup(lineup):
    pitch = VerticalPitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(6, 8))

    ax.set_ylim(-1, 60)

    for _, player in lineup.iterrows():
        x, y = _get_position_coordinates(player['starting_position'])
        display_name = player['player_nickname'] if pd.notnull(player['player_nickname']) else player['player_name']

        pitch.scatter(x, y, s=300, ax=ax, color='royalblue')
        pitch.annotate(display_name, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')

    plt.title('Formacja 4-3-3')

    plt.show()

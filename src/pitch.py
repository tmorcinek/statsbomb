import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import VerticalPitch


def _get_position_coordinates(position_name):
    positions = {
        # Goalkeeper
        'Goalkeeper': (5, 40),

        # Defenders
        'Left Back': (15, 10),
        'Left Wing Back': (20, 15),
        'Left Center Back': (15, 30),
        'Center Back': (15, 40),
        'Right Center Back': (15, 50),
        'Right Back': (15, 70),
        'Right Wing Back': (20, 65),

        # Defensive Midfield
        'Left Defensive Midfield': (25, 25),
        'Center Defensive Midfield': (25, 40),
        'Right Defensive Midfield': (25, 55),

        # Central Midfield
        'Left Center Midfield': (35, 30),
        'Right Center Midfield': (35, 50),

        # Wide Midfielders
        'Left Midfield': (35, 20),
        'Right Midfield': (35, 60),

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


def _add_coordinates(df):
    df = df.copy()
    df[['x', 'y']] = df['starting_position'].apply(
        lambda pos: pd.Series(_get_position_coordinates(pos))
    )
    return df


def display_starting_lineup(lineup):
    # Create a vertical pitch
    pitch = VerticalPitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(6, 8))
    # Show only the bottom half
    # If pitch length is 120, this would show from y=60 to y=120
    ax.set_ylim(-1, 60)

    lineup = _add_coordinates(lineup)

    for _, player in lineup.iterrows():
        x = player['x']
        y = player['y']
        position = player['player_nickname']

        pitch.scatter(x, y, s=300, ax=ax)
        pitch.annotate(position, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')

    plt.title('Formacja 4-3-3')

    plt.show()

from matplotlib import pyplot as plt
from mplsoccer import VerticalPitch


def get_position_coordinates(position_name):
    positions = {
        # Goalkeeper
        'Goalkeeper': (5, 40),

        # Defenders
        'Left Back': (15, 20),
        'Left Wing Back': (15, 25),
        'Left Center Back': (15, 30),
        'Center Back': (15, 40),
        'Right Center Back': (15, 50),
        'Right Back': (15, 60),
        'Right Wing Back': (15, 55),

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
        'Left Wing': (55, 20),
        'Left Center Forward': (55, 30),
        'Center Forward': (55, 40),
        'Right Center Forward': (55, 50),
        'Right Wing': (55, 60)
    }

    return positions.get(position_name, None)

def display_half_pitch():
    # Create a vertical pitch
    pitch = VerticalPitch(pitch_type='statsbomb', half=True)
    fig, ax = pitch.draw(figsize=(12, 8))
    # Show only the bottom half
    # If pitch length is 120, this would show from y=60 to y=120
    ax.set_ylim(-1, 60)

    positions = {
        'Goalkeeper': (8, 40),
        'Left Back': (20, 10),
        'Left Center Back': (20, 30),
        'Right Center Back': (20, 50),
        'Right Back': (20, 70),
        'Left Midfield': (38, 20),
        'Center Midfield': (38, 40),
        'Right Midfield': (38, 60),
        'Left Wing': (56, 10),
        'Center Forward': (56, 40),
        'Right Wing': (56, 70)
    }
    for position, (x, y) in positions.items():
        pitch.scatter(x, y, s=300, ax=ax)
        pitch.annotate(position, (x, y), ax=ax, ha='center', va='center', fontsize=8, color='black')
    plt.title('Formacja 4-3-3')


    plt.show()

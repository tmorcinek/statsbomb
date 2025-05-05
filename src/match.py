import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import Pitch

from statsbombpy.local import get_data


def display_shots(match_id):
    df = pd.DataFrame(get_data(f"events/{match_id}.json"))

    df['type_name'] = df['type'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
    df['team_name'] = df['team'].apply(lambda x: x['name'] if isinstance(x, dict) else None)

    shots = df[df['type_name'] == 'Shot']

    pitch = Pitch(line_color='black', pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(10, 7))

    for _, shot in shots.iterrows():
        x, y = shot['location']  # Lokalizacja strzału
        team = shot['team_name']  # Nazwa drużyny
        color = 'blue' if team == 'Barcelona' else 'red'  # Wybór koloru
        # if team != 'Barcelona':
        pitch.scatter(x, y, alpha=0.7, s=100, color=color, ax=ax)

    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Barcelona'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Deportivo Alavés')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=True)

    ax.set_title('Lokalizacje Strzałów', fontsize=14)
    fig.show()

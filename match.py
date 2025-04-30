import json
import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import Pitch


def display_shots(events_json):
    with open(events_json, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Przekształć dane na DataFrame
    df = pd.DataFrame(data)

    # Rozpakuj typ wydarzenia (np. strzały, podania)
    df['type_name'] = df['type'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
    df['team_name'] = df['team'].apply(lambda x: x['name'] if isinstance(x, dict) else None)

    # Filtrowanie wydarzeń do strzałów
    shots = df[df['type_name'] == 'Shot']

    # Wizualizacja: rysowanie boiska
    pitch = Pitch(line_color='black', pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Dodanie strzałów do wizualizacji
    for _, shot in shots.iterrows():
        x, y = shot['location']  # Lokalizacja strzału
        team = shot['team_name']  # Nazwa drużyny
        color = 'blue' if team == 'Barcelona' else 'red'  # Wybór koloru
        # if team != 'Barcelona':
        pitch.scatter(x, y, alpha=0.7, s=100, color=color, ax=ax)

    # Dodanie legendy
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Barcelona'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Deportivo Alavés')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=True)

    # Wyświetlenie wizualizacji
    ax.set_title('Lokalizacje Strzałów', fontsize=14)
    fig.show()


def print_match(match_id):
    with open('../open-data/data/events/3938637.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    data = [record for record in data if 'shot' in record]
    df = pd.DataFrame(data)
    # df = pd.json_normalize(
    #     data,
    #     record_path=['shot'],  # Expand the freeze_frame
    #     meta=[
    #         'id', 'index', 'timestamp', 'minute', 'second',
    #         ['type', 'name'], ['possession_team', 'name'], ['shot', 'outcome', 'name']
    #     ],
    #     meta_prefix='meta.',
    # )
    # df = pd.json_normalize(
    #     data,
    #     meta=[['type', 'name']],
    #     errors='ignore'  # Ignore missing keys
    # )

    # Display the flattened structure
    print(df)
    # shots = df[(df['type.name'] == "Shot") & (df['shot.outcome.name'] == "Goal")]


    # print(shots)

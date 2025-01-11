import matplotlib.pyplot as plt
import json
import pandas as pd
from mplsoccer.pitch import Pitch


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


def print_events(events_json):
    with open(events_json, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Przekształć dane na DataFrame
    df = pd.DataFrame(data)

    # Rozpakuj typ wydarzenia
    df['type_name'] = df['type'].apply(lambda x: x['name'] if isinstance(x, dict) else None)

    # Wyciągnij unikalne rodzaje eventów
    event_types = df['type_name'].unique()
    print("Rodzaje wydarzeń:", event_types)

    # (Opcjonalnie) policz, ile jest każdego typu wydarzenia
    event_counts = df['type_name'].value_counts()
    print("\nLiczba każdego typu wydarzenia:\n", event_counts)


def print_competitions():
    with open('../open-data/data/competitions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df = pd.DataFrame(data)
    df = df[df['competition_gender'] == 'male']
    df = df[['competition_id', 'competition_name', 'season_name']]
    df = df.sort_values(by='season_name', ascending=False)

    print(df)

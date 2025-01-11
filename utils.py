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
    df = df[['competition_id', 'competition_name', 'season_name', 'season_id']]
    df = df.sort_values(by='season_name', ascending=False)

    print(df)


def print_competition(competition_id, season_id):
    with open(f'../open-data/data/matches/{competition_id}/{season_id}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df = pd.DataFrame(data)
    team_id = 904
    team_name = 'Bayer Leverkusen'
    df['home_team_name'] = df['home_team'].apply(lambda x: x['home_team_name'] if isinstance(x, dict) else None)
    df['home_team_id'] = df['home_team'].apply(lambda x: x['home_team_id'] if isinstance(x, dict) else None)
    df['away_team_name'] = df['away_team'].apply(lambda x: x['away_team_name'] if isinstance(x, dict) else None)
    df['away_team_id'] = df['away_team'].apply(lambda x: x['away_team_id'] if isinstance(x, dict) else None)
    df['score'] = df.apply(lambda row: f"{row['home_score']}:{row['away_score']}", axis=1)
    df = df.sort_values(by='match_date', ascending=True)

    def calculate_points(row):
        home_score = row['home_score']
        away_score = row['away_score']
        home_team_id = row['home_team_id']
        away_team_id = row['away_team_id']
        if home_score == away_score:
            return 1
        elif (home_team_id == team_id and home_score > away_score) or (
                away_team_id == team_id and away_score > home_score):
            return 3
        else:
            return 0

    df['points'] = df.apply(calculate_points, axis=1)

    goals_scored = df[df['home_team_id'] == team_id]['home_score'].sum() + df[df['away_team_id'] == team_id][
        'away_score'].sum()
    goals_against = df[df['home_team_id'] != team_id]['home_score'].sum() + df[df['away_team_id'] != team_id][
        'away_score'].sum()
    wins = (df['points'] == 3).sum()
    draws = (df['points'] == 1).sum()
    loses = (df['points'] == 0).sum()
    form = list(map(lambda x: {3: 'Win', 1: 'Draw', 0: 'Loss'}[x], df.tail(5)['points'].tolist()))

    df = df[['match_id', 'match_date', 'home_team_name', 'away_team_name', 'score', 'points']]

    print(df)

    team_data = {
        'team_id': team_id,
        'team_name': team_name,
        'matches_played': len(df),
        'wins': wins,
        'draws': draws,
        'loses': loses,
        'goals_scored': goals_scored,
        'goals_against': goals_against,
        'goals_difference': goals_scored - goals_against,
        'points': df['points'].sum(),
        'form': form
    }
    team_df = pd.DataFrame([team_data])

    print(team_df)

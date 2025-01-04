import json
import pandas as pd
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt


if __name__ == '__main__':

    with open('../open-data/data/events/15946.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Przekształć dane na DataFrame
    df = pd.DataFrame(data)

    # Rozpakuj typ wydarzenia (np. strzały, podania)
    df['type_name'] = df['type'].apply(lambda x: x['name'] if isinstance(x, dict) else None)

    # Filtrowanie wydarzeń do strzałów
    shots = df[df['type_name'] == 'Shot']

    # Wizualizacja: rysowanie boiska
    pitch = Pitch(line_color='black', pitch_type='statsbomb')
    fig, ax = pitch.draw(figsize=(10, 7))

    # Dodanie strzałów do wizualizacji
    for _, shot in shots.iterrows():
        x, y = shot['location']  # Lokalizacja strzału
        pitch.scatter(x, y, alpha=0.7, s=100, color='red', ax=ax)

    # Wyświetlenie wizualizacji
    ax.set_title('Lokalizacje Strzałów', fontsize=14)
    fig.show()
    plt.show()

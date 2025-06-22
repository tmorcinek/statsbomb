import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mplsoccer import Pitch

import seaborn as sns
import src.events.data as dt
from statsbombpy import sb
from collections import defaultdict

pitch_length = 120
pitch_width = 80


def get_zone(x, y, grid_x=16, grid_y=12):
    zone_x = int(min(x / pitch_length * grid_x, grid_x - 1))
    zone_y = int(min(y / pitch_width * grid_y, grid_y - 1))
    return zone_x, zone_y


def get_competition_passes(competition_id: int = 55, season_id: int = 282):
    matches = sb.matches(competition_id, season_id)

    all_passes = []

    for match_id in matches['match_id']:
        passes = sb.events(match_id).passes().dropna(axis=1, how='all')
        all_passes.append(passes)

    return pd.concat(all_passes, ignore_index=True)

def get_competition_carries(competition_id: int = 55, season_id: int = 282):
    matches = sb.matches(competition_id, season_id)

    all_carries = []

    for match_id in matches['match_id']:
        events = sb.events(match_id, filters= {"type": "Carry"})
        carries = events.dropna(axis=1, how='all')
        all_carries.append(carries)

    return pd.concat(all_carries, ignore_index=True)

def get_competition_shots(competition_id: int = 55, season_id: int = 282, own_goals_included=False):
    matches = sb.matches(competition_id, season_id)

    all_shots = []

    for match_id in matches['match_id']:
        events = sb.events(match_id)
        shots_df = events.shots()
        if own_goals_included:
            shots_df = shots_df + dt.own_goals_from_events(events)
        all_shots.append(shots_df)

    return pd.concat(all_shots, ignore_index=True).dropna(axis=1, how='all')


def get_competition_goals(competition_id: int = 55, season_id: int = 282):
    matches = sb.matches(competition_id, season_id)

    all_goals_df = []
    for idx, row in matches.iterrows():
        goals = dt.goals(row['match_id'], True)
        all_goals_df.append(goals)

    return pd.concat(all_goals_df, ignore_index=True).dropna(axis=1, how='all')

def create_transitions(events, transition_counts = None):
    if transition_counts is not None:
        transition_counts = defaultdict(lambda: defaultdict(int))

    for event in events:
        x, y = event['location']
        start_zone = get_zone(event["start_x"], event["start_y"])
        end_zone = get_zone(event["end_x"], event["end_y"])

        # Pomijamy przypadki braku przemieszczenia
        if start_zone != end_zone:
            transition_counts[start_zone][end_zone] += 1


def transition(event: pd.Series):
    start_zone = get_zone(*(event['location']))
    match event['type']:
        case "Carry":
            return start_zone, get_zone(*event['carry_end_location'])
        case "Pass":
            return start_zone, get_zone(*event['pass_end_location'])
        case _:
            raise ValueError(f"Unsupported event type: {event['type']}")


def plot_xt_zones_2():
    pitch = Pitch(line_zorder=2, pitch_color='black')
    fig, ax = pitch.draw()

    # Manually define the shape (12 vertical bins, 16 horizontal bins)
    stats = {
        'statistic': np.zeros((12, 16)),
        'x_grid': np.linspace(0, 120, 17),  # 16 bins = 17 edges
        'y_grid': np.linspace(0, 80, 13),   # 12 bins = 13 edges
    }

    # Set only the selected zones
    stats['statistic'][5, 4] = 1  # (y_idx=5, x_idx=4)
    stats['statistic'][3, 5] = 1  # (y_idx=3, x_idx=5)

    pitch.heatmap(stats, edgecolors='black', cmap='hot', ax=ax)
    plt.show()


def plot_xt_zones_positional():
    pitch = Pitch(line_zorder=2, pitch_color='black')
    fig, ax = pitch.draw()
    x = np.random.uniform(low=0, high=120, size=100)
    y = np.random.uniform(low=0, high=80, size=100)
    stats = pitch.bin_statistic_positional(x, y)
    pitch.heatmap_positional(stats, edgecolors='black', cmap='hot', ax=ax)
    plt.show()

def plot_xt_zones():
    pitch_length = 120  # Example: 120 units long
    pitch_width = 80  # Example: 80 units wide
    bin_size_x = 10  # Example: 10 units wide bins
    bin_size_y = 10  # Example: 10 units tall bins

    # Calculate number of bins
    num_bins_x = int(pitch_length / bin_size_x)
    num_bins_y = int(pitch_width / bin_size_y)

    # Create grid
    x_grid = np.linspace(0, pitch_length, num_bins_x + 1)
    y_grid = np.linspace(0, pitch_width, num_bins_y + 1)

    # Example data (replace with your actual data)
    # Assuming you have a list of x, y coordinates (e.g., player positions)
    data = np.array([
        [10, 15], [20, 25], [30, 35], [40, 45], [50, 55], [60, 65], [70, 75],
        [15, 20], [25, 30], [35, 40], [45, 50], [55, 60], [65, 70], [75, 77],
        [20, 25], [30, 35], [40, 45], [50, 55], [60, 65], [70, 75], [80, 77],
    ])

    # Using numpy.histogram2d (or similar methods like mplsoccer.bin_statistic)
    H, _, _ = np.histogram2d(data[:, 0], data[:, 1], bins=[x_grid, y_grid])

    total_points = len(data)
    heatmap_data = H / total_points

    pitch = Pitch(pitch_length=pitch_length, pitch_width=pitch_width)
    fig, ax = pitch.draw(figsize=(10, 6.67))

    # Plot the heatmap (using seaborn's heatmap or pitch.heatmap)
    # Using mplsoccer:
    pitch.heatmap(heatmap_data, x_grid, y_grid, ax=ax, cmap='hot', edgecolors='#666666')

    # Using seaborn:
    sns.heatmap(heatmap_data.T, xticklabels=False, yticklabels=False, cmap='hot', ax=ax, cbar=False, linewidth=0, alpha=0.1)

    # Add title and labels (optional)
    # ax.set_title("Player Movement Heatmap", fontsize=16)

    plt.show()

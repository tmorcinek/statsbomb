import pandas as pd

import src.events.data as dt
from statsbombpy import sb

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

def get_competition_shots(competition_id: int = 55, season_id: int = 282, own_goals_included=False):
    matches = sb.matches(competition_id, season_id)

    all_shots = []

    for match_id in matches['match_id']:
        events = sb.events(match_id)
        shots_df = events.shots()
        if own_goals_included:
            shots_df = pd.concat([shots_df, dt.own_goals_from_events(events)], ignore_index=True)
        all_shots.append(shots_df)

    return pd.concat(all_shots, ignore_index=True).dropna(axis=1, how='all')


def get_competition_goals(competition_id: int = 55, season_id: int = 282):
    matches = sb.matches(competition_id, season_id)

    all_goals_df = []
    for idx, row in matches.iterrows():
        goals = dt.goals(row['match_id'], True)
        all_goals_df.append(goals)

    return pd.concat(all_goals_df, ignore_index=True).dropna(axis=1, how='all')

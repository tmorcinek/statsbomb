import numpy as np
import pandas as pd

from statsbombpy import sb


def relevant_events(match_id) -> pd.DataFrame:
    events = sb.events(match_id)
    return filter_relevant_events(events)


def filter_relevant_events(events) -> pd.DataFrame:
    return events[~events['type'].isin([
        'Substitution', 'Injury Stoppage', 'Half Start', 'Half End',
        'Tactical Shift', 'Referee Ball-Drop', 'Starting XI'
    ])].sort_values(by=['index'])
    # events = events.sort_values(by=['period', 'timestamp'])


def teams(events: pd.DataFrame) -> dict:
    df = events[events['type'] == "Starting XI"][['team', 'team_id']]
    return df.set_index('team')['team_id'].to_dict()


def event_info(event: pd.Series) -> pd.Series:
    return event[['type', 'player', 'team', 'possession', 'possession_team', 'timestamp']]


def event_info_string(event: pd.Series) -> str:
    return (f"Half:{event['period']} [{event['timestamp']}] {event['team']} ({event['possession_team']} in possession #{event['possession']})\n"
            f"{event['player']} performs {event['type']}")


def unique_possessions(events: pd.DataFrame) -> pd.Series:
    return events['possession'].nunique()


def unique_possessions_by_team(events: pd.DataFrame) -> pd.Series:
    events['possession_team_name'] = events['possession_team'].apply(
        lambda x: x['name'] if isinstance(x, dict) else x
    )
    return events.groupby('possession_team_name')['possession'].nunique()


def players(events: pd.DataFrame) -> np.ndarray:
    return events.player.dropna().unique()


def types(events: pd.DataFrame) -> np.ndarray:
    return events.type.unique()


from pandas.api.extensions import register_dataframe_accessor


@register_dataframe_accessor("shots")
class ShotsAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def __call__(self) -> pd.DataFrame:
        return self._obj[self._obj['type'] == 'Shot']


@register_dataframe_accessor("passes")
class PassesAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def __call__(self) -> pd.DataFrame:
        return self._obj[self._obj['type'] == 'Pass']

import pandas as pd

from statsbombpy import sb


def relevant_events(match_id) -> pd.DataFrame:
    events = sb.events(match_id)
    events = events[~events['type'].isin([
        'Substitution', 'Injury Stoppage', 'Half Start', 'Half End',
        'Tactical Shift', 'Referee Ball-Drop', 'Starting XI'
    ])]
    return events

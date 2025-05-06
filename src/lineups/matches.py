import src.lineups.lineups as ln
import src.lineups.pitch as pt
from statsbombpy import sb


def extract_match_title(row):
    return (
        f"{row['competition']} - {row['season']}\n"
        f"{row['competition_stage']}\n"
        f"{row['home_team']} {row['home_score']}:{row['away_score']} {row['away_team']}\n"
        f"{row['match_date']}, {row['kick_off'][:5]} {row['stadium']}\n"
        f"Referee: {row['referee']}"
    )


def display_competition_lineups(show_half_pitches=False):
    matches = sb.matches(55, 282)
    for _, match in matches.iterrows():
        match_id = match['match_id']
        pt.display_starting_lineups(match_id, extract_match_title(match))
        positions = ln.starting_lineups(match_id)
        if show_half_pitches:
            for key, value in positions.items():
                pt.display_starting_lineup(key, value)


def display_match_lineups(match_id: int, competition_id: int = None, season_id: int = None):
    if competition_id and season_id:
        title = extract_match_title(sb.matches(55, 282).query("match_id == @match_id").squeeze())
    else:
        title = None
    pt.display_starting_lineups(match_id, title)

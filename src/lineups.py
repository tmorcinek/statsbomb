from statsbombpy import sb


def starting_lineups(match_id) -> dict:
    return {
        team_name: players.loc[
            players['positions'].apply(lambda x: len(x) > 0 and x[0].get('start_reason') == 'Starting XI')
        ].assign(
            starting_position=lambda df: df['positions'].apply(lambda pos: pos[0]['position'])
        ).copy()
        for team_name, players in sb.lineups(match_id).items()
    }


def unique_positions(match_id) -> set:
    return {
        pos
        for players in starting_lineups(match_id).values()
        for pos in players['starting_position'].explode()
    }

def unique_positions_matches(competition_id: int, season_id: int) -> set:
    matches  = sb.matches(competition_id, season_id)
    positions = set()
    for match_id in matches['match_id'].to_list():
        positions.update(unique_positions(match_id))
    return positions

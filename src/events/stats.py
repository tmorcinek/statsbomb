from pandas import DataFrame

from statsbombpy import sb


def get_events(match_id) -> DataFrame:
    return sb.events(match_id)

def get_events_of_type(events_df, event_type: str) -> DataFrame:
    return events_df[events_df['type'] == event_type]


def team_stats_summary(df):
    teams = df['team'].dropna().unique()
    if len(teams) != 2:
        raise ValueError("Expected exactly 2 teams in the DataFrame.")

    team_stats = {team: {} for team in teams}

    # Possession: based on count of possessions
    possession_counts = df.groupby('possession_team').ngroups
    total_possessions = df['possession'].nunique()
    for team in teams:
        team_possessions = df[df['possession_team'] == team]['possession'].nunique()
        team_stats[team]['Possession (%)'] = round(100 * team_possessions / total_possessions, 1)

    # Total attempts
    shots = df[df['type'] == 'Shot']
    for team in teams:
        team_stats[team]['Total attempts'] = len(shots[shots['team'] == team])

    # Attacks = number of possessions
    for team in teams:
        team_stats[team]['Attacks'] = df[df['possession_team'] == team]['possession'].nunique()

    # Corners taken
    corners = df[df['play_pattern'] == 'From Corner']
    for team in teams:
        team_stats[team]['Corners taken'] = len(corners[corners['team'] == team])

    # Passing stats
    passes = df[(df['type'] == 'Pass') & (df['pass_type'].isna() | df['pass_type'].isin(['Recovery']))]
    for team in teams:
        team_passes = passes[passes['team'] == team]
        attempted = len(team_passes)
        completed = len(team_passes[team_passes['pass_outcome'].isna()])  # successful passes have NaN outcome
        accuracy = 100 * completed / attempted if attempted > 0 else 0
        team_stats[team]['Passes attempted'] = attempted
        team_stats[team]['Passes completed'] = completed
        team_stats[team]['Passing accuracy (%)'] = round(accuracy, 1)

    # Balls recovered
    for team in teams:
        team_stats[team]['Balls recovered'] = len(df[(df['type'] == 'Ball Recovery') & (df['team'] == team)])

    # Offsides
    for team in teams:
        team_stats[team]['Offsides'] = len(df[(df['type'] == 'Offside') & (df['team'] == team)])

    # Saves
    for team in teams:
        team_stats[team]['Saves'] = len(shots[(shots['team'] != team) & (shots['shot_outcome'] == 'Saved')])
        # team_stats[team]['Saves'] = len(df[(df['type'] == 'Save') & (df['team'] == team)])

    # Yellow/Red cards
    # for team in teams:
    #     team_cards = df[(df['type'] == 'Foul Committed') & (df['team'] == team)]
    #     yellow = team_cards[team_cards['foul_card'] == 'Yellow Card']
    #     red = team_cards[team_cards['foul_card'] == 'Red Card']
    #     team_stats[team]['Yellow cards'] = len(yellow)
    #     team_stats[team]['Red cards'] = len(red)

    return team_stats

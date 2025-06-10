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

        # Shots on target
        shots_on_target = shots[
            (shots['team'] == team) &
            (shots['shot_outcome'].isin(['Saved', 'Goal']))
        ]
        team_stats[team]['Shots on target'] = len(shots_on_target)

        # Goals
        goals = shots[
            (shots['team'] == team) &
            (shots['shot_outcome'] == 'Goal')
        ]
        team_stats[team]['Goals'] = len(goals)

    # Attacks = number of possessions
    for team in teams:
        team_stats[team]['Attacks'] = df[df['possession_team'] == team]['possession'].nunique()

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

    # Dribbles
    for team in teams:
        team_stats[team]['Dribbles'] = len(df[(df['type'] == 'Dribble') & (df['team'] == team)])

    # Saves
    for team in teams:
        team_stats[team]['Saves'] = len(shots[(shots['team'] != team) & (shots['shot_outcome'] == 'Saved')])
        team_stats[team]['Blocks'] = len(shots[(shots['team'] != team) & (shots['shot_outcome'] == 'Blocked')])
        # team_stats[team]['Saves'] = len(df[(df['type'] == 'Save') & (df['team'] == team)])

    # Set piece types via pass_type
    pass_events = df[df['type'] == 'Pass']
    for team in teams:
        team_passes = pass_events[pass_events['team'] == team]
        team_stats[team]['Goal Kicks'] = len(team_passes[team_passes['pass_type'] == 'Goal Kick'])
        team_stats[team]['Throw-ins'] = len(team_passes[team_passes['pass_type'] == 'Throw-in'])
        team_stats[team]['Corners taken'] = len(team_passes[team_passes['pass_type'] == 'Corner'])
        team_stats[team]['Free Kicks'] = len(team_passes[team_passes['pass_type'] == 'Free Kick'])

    # Fouls and Yellow Cards
    fouls = df[df['type'] == 'Foul Committed']
    for team in teams:
        team_fouls = fouls[fouls['team'] == team]
        team_stats[team]['Fouls committed'] = len(team_fouls)
        team_stats[team]['Yellow cards'] = len(team_fouls[team_fouls['foul_committed_card'] == 'Yellow Card'])
        team_stats[team]['Red cards'] = len(team_fouls[team_fouls['foul_committed_card'] == 'Red Card'])

    # Yellow/Red cards
    # for team in teams:
    #     team_cards = df[(df['type'] == 'Foul Committed') & (df['team'] == team)]
    #     yellow = team_cards[team_cards['foul_card'] == 'Yellow Card']
    #     red = team_cards[team_cards['foul_card'] == 'Red Card']
    #     team_stats[team]['Yellow cards'] = len(yellow)
    #     team_stats[team]['Red cards'] = len(red)

    return team_stats

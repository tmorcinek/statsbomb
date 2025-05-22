import pandas as pd

from statsbombpy import sb


def print_events_info(match_id):
    df = sb.events(match_id)

    event_types = df['type'].unique()
    print("Rodzaje wydarzeń:", event_types)

    event_counts = df['type'].value_counts()
    print("\nLiczba każdego typu wydarzenia:\n", event_counts)
    print(len(event_counts))


def get_events_type_counts(match_id) -> pd.Series:
    return sb.events(match_id)['type'].value_counts()


def get_events_type_unique(match_id) -> set[str]:
    return set(sb.events(match_id)['type'].unique())


def get_competition_data(competition_id, season_id):
    competition = sb.competitions()
    competition = competition[(competition['competition_id'] == competition_id) & (competition['season_id'] == season_id)]
    return competition.squeeze()


def get_competition_info(competition_id, season_id) -> tuple[pd.Series, pd.DataFrame]:
    competition = get_competition_data(competition_id, season_id)

    df = sb.matches(competition_id, season_id)
    df = df.sort_values(by='match_date', ascending=True)
    df['score'] = df.apply(lambda row: f"{row['home_score']}:{row['away_score']}", axis=1)
    df = df[['match_id', 'match_date', 'home_team', 'away_team', 'score', 'home_score', 'away_score']]

    return competition, df


def print_competition_info(competition_id, season_id):
    competition, matches = get_competition_info(competition_id, season_id)
    print(
        f"{competition['competition_name']} {competition['season_name']}, {competition['competition_gender']} (competition_id: {competition['competition_id']}, season_id: {season_id})")
    print(matches)


def print_competition_bayer():
    competition_id = 9
    season_id = 281
    competition, df = get_competition_info(competition_id, season_id)
    print("competition:\n", competition)

    team_name = "Bayer Leverkusen"

    def calculate_points(row):
        home_score = row['home_score']
        away_score = row['away_score']
        home_team = row['home_team']
        away_team = row['away_team']
        if home_score == away_score:
            return 1
        elif (home_team == team_name and home_score > away_score) or (
                away_team == team_name and away_score > home_score):
            return 3
        else:
            return 0

    df['points'] = df.apply(calculate_points, axis=1)

    goals_scored = df[df['home_team'] == team_name]['home_score'].sum() + df[df['away_team'] == team_name][
        'away_score'].sum()
    goals_against = df[df['home_team'] != team_name]['home_score'].sum() + df[df['away_team'] != team_name][
        'away_score'].sum()
    wins = (df['points'] == 3).sum()
    draws = (df['points'] == 1).sum()
    loses = (df['points'] == 0).sum()
    form = list(map(lambda x: {3: 'Win', 1: 'Draw', 0: 'Loss'}[x], df.tail(5)['points'].tolist()))

    df = df[['match_id', 'match_date', 'home_team', 'away_team', 'score', 'points']]

    print(df)

    team_data = {
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
    print(pd.DataFrame([team_data]))

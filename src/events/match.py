from matplotlib import pyplot as plt
from mplsoccer import Pitch

from src.lineups.matches import display_match_lineups
from statsbombpy import sb


def display_goals(match_id):
    display_match_lineups(match_id, 55, 282)
    events = sb.events(match_id)
    goals = events[events['shot_outcome'] == 'Goal']
    goals = goals.dropna(axis=1, how='all')
    print(goals)
    plot_shots(events[events['type'] == 'Shot'], "Shots")


def plot_shots_by_team(df, title="Shots Map by Team"):
    teams = df['team'].unique()
    if len(teams) != 2:
        raise ValueError("DataFrame must contain exactly two teams.")

    home_team, away_team = teams

    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black', half=True)
    fig, axes = pitch.draw(nrows=1, ncols=2, figsize=(16, 8))

    for ax, team in zip(axes, [home_team, away_team]):
        team_df = df[df['team'] == team]

        for _, row in team_df.iterrows():
            x, y = row['location']
            end_x, end_y, *_ = row['shot_end_location']
            outcome = row['shot_outcome']
            xg = row.get('shot_statsbomb_xg', None)

            color = {
                'Goal': 'green',
                'Saved': 'blue',
                'Off T': 'red',
                'Blocked': 'gray'
            }.get(outcome, 'black')

            pitch.arrows(x, y, end_x, end_y, width=2, headwidth=6, color=color, ax=ax, label=outcome)

            if xg:
                ax.text(x, y - 2, f"{xg:.2f}", ha='center', fontsize=8, color='black')

        ax.set_title(f"{team}", fontsize=14)

        if ax == axes[0]:
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys(), loc='lower left')

    fig.suptitle(title, fontsize=18)
    plt.tight_layout()
    plt.show()


def plot_shots(df, title="Shots Map"):
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black')
    fig, ax = pitch.draw(figsize=(12, 8))

    for _, row in df.iterrows():
        x, y = row['location']
        end_x, end_y, *_ = row['shot_end_location']
        outcome = row['shot_outcome']
        xg = row.get('shot_statsbomb_xg', None)

        color = {
            'Goal': 'green',
            'Saved': 'blue',
            'Off T': 'red',
            'Blocked': 'gray'
        }.get(outcome, 'black')

        pitch.arrows(x, y, end_x, end_y, width=2, headwidth=6, color=color, ax=ax, label=outcome)

        if xg:
            ax.text(x, y - 2, f"{xg:.2f}", ha='center', fontsize=9, color='black')

    ax.set_title(title, fontsize=16)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='lower left')

    plt.show()

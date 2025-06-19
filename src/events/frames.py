import pandas as pd
from mplsoccer import Pitch


def get_frames_for_event(event_row: pd.Series, frames_df: pd.DataFrame) -> pd.DataFrame:
    return frames_df[frames_df['id'] == event_row['id']]


def plot_polygon(points, pitch=None, ax=None, color='red', linewidth=1.5):
    if pitch is None or ax is None:
        pitch = Pitch(pitch_type='statsbomb')
        fig, ax = pitch.draw(figsize=(10, 7))

    for i in range(0, len(points) - 2, 2):
        x_start, y_start = points[i], points[i + 1]
        x_end, y_end = points[i + 2], points[i + 3]
        pitch.lines(x_start, y_start, x_end, y_end, ax=ax, color=color, linewidth=linewidth)


def plot_frame_group(frame_group: pd.DataFrame, pitch=None, ax=None, title=None):
    if pitch is None or ax is None:
        pitch = Pitch(pitch_type='statsbomb')
        fig, ax = pitch.draw(figsize=(10, 7))

    if title:
        ax.set_title(title, fontsize=16)

    plot_polygon(frame_group.iloc[0]['visible_area'], pitch, ax)

    def node_color(row):
        if row['actor']:
            return 'chartreuse'
        elif row['teammate']:
            return 'blue'
        else:
            return 'yellow'

    def edge_color(row):
        if row['keeper']:
            return 'magenta'
        else:
            return 'black'

    color = frame_group.apply(node_color, axis=1)
    edge_colors = frame_group.apply(edge_color, axis=1)
    locations = frame_group['location'].apply(pd.Series)
    pitch.scatter(locations[0], locations[1], ax=ax, color=color, s=100, edgecolors=edge_colors)

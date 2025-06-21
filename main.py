import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch

import src.events.match as m
import src.lineups.lineups as ln
import src.events.stats as st
import src.events.data as dt
import src.events.frames as fr
from statsbombpy import sb


def print_euro_matches():
    print(sb.matches(55, 282))


def print_events():
    match_df = sb.events(3938637)
    # print(match_df.drop(4).head(10))
    print(match_df.shape)
    print(len(match_df.columns))
    match_df_nonflat = sb.events(3938637, flatten_attrs=False)
    # print(match_df.drop(4).head(10))
    print(match_df_nonflat.shape)
    print(len(match_df_nonflat.columns))
    main_set = set(match_df.columns.to_list())
    print(f"Flatten set: {main_set}")
    non_flat_set = set(match_df_nonflat.columns.to_list())
    print(f"Normal set: {non_flat_set}")
    print("Dzilania: ")
    union = main_set.union(non_flat_set)
    print(union)
    print(len(union))
    intersection = main_set.issubset(non_flat_set)
    print(intersection)
    print(match_df_nonflat.drop(6).head(10)['type'])


def events_and_frames(match_id):
    events = dt.relevant_events(match_id).head(20)
    # events = events.sort_values(by=['period', 'minute', 'second']).reset_index(drop=True)
    events = events.sort_values(by=['index']).reset_index(drop=True)
    frames = sb.frames(match_id)
    print(events.dropna(axis=1, how='all'))
    for index, event in events.iterrows():
        frames_for_event = fr.get_frames_for_event(event, frames)
        if frames_for_event.empty:
            print(f"{index} DataFrame for key={event['type']} is empty, {frames_for_event.shape}")
        else:
            pitch = Pitch(pitch_type='statsbomb')
            fig, ax = pitch.draw(figsize=(10, 7))

            fr.plot_frame_group(frames_for_event, pitch, ax, title=dt.event_info_string(event))
            if event['type']== "Pass":
                fr.draw_pass(pitch, ax, event)
            plt.show()

        # print(f"{index} {event['id']}, {event['type']}")
        # print(f"{index} {event['id']}, {frames_for_event}")




if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # utl.print_competition_info(55, 282)

    match_id = 3943043  ## final
    # match_id = 3930167 ## all the event types

    # events = events.dropna(axis=1, how='all')
    events_and_frames(match_id)
    events = sb.events(match_id)
    # events = events[events['type'] == "Starting XI"]
    # print(events.dropna(axis=1, how="all"))
    print(dt.teams(events))

    # events_with_freeze_frame = events_without_frames[events_without_frames['freeze_frame'].isna()]
    # team_passes[team_passes['pass_outcome'].isna()]

    # print(f"{len(events_with_freeze_frame)} eventów bez frames zawiera freeze_frame.")
    # print(events_with_freeze_frame[['id', 'type', 'freeze_frame']].head(3))
    # print(frames.head(20))


    # print(df.keys())
    # print(df.shape)

    # df = sb.events(3943043)
    #
    # print(df.head(20))
    # print(df.shape)
    # df = df[df['type'] == 'Foul Committed']
    # print(df.dropna(axis=1, how='all'))
    # df = st.get_events_of_type(df, 'Bad Behaviour')


    # turkey_match_id = 3942382
    # dennmark_match_id = 3930171
    # belgium_match_id = 3941019
    # switzerland_match_id = 3940878

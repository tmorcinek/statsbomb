import src.events.data as dt
from statsbombpy import sb


def finding_irrelevant_data():
    match_id = 3943043  ## final

    events = dt.relevant_events(match_id)
    frames = sb.frames(match_id)
    # events_and_frames(3943043)
    event_ids_with_frames = frames['id'].unique()
    events_with_frames = events[events['id'].isin(event_ids_with_frames)]
    events_without_frames = events[~events['id'].isin(event_ids_with_frames)]
    print(f"{len(events_with_frames)} / {len(events)} events have frames.")
    print(f"{len(events_without_frames)} / {len(events)} events does not have frames.")
    passes_without_frames = events_without_frames[events_without_frames['type'] == "Pass"]
    passes = events[events['type'] == "Pass"]
    value_counts = passes_without_frames['pass_outcome'].value_counts(dropna=False)
    events_value_counts = events_without_frames['type'].value_counts(dropna=False)
    # m.plot_passes(passes_without_frames)
    print(f"value_counts:{value_counts}, pass_count:{len(passes_without_frames)}")
    print(f"events_without_frame_value_counts:{events_value_counts}")
    print(f"events_value_counts:{events['type'].value_counts(dropna=False)}")
    events_head = events.head(20)
    print(f"{events_head}")

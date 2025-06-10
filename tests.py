import unittest

import pandas as pd
from matplotlib import pyplot as plt

import src.events.match as m
import src.utils as utl
from src.frames import plot_polygon, plot_frame_group
from src.lineups.lineups import starting_lineups, unique_positions, _unique_positions_matches
from src.lineups.matches import extract_match_title, display_match_lineups
from src.lineups.pitch import _get_position_coordinates, display_starting_lineup, display_starting_lineups
from src.utils import get_competition_info, get_events_type_counts, get_events_type_unique
from statsbombpy import sb


class StatsbombPyTests(unittest.TestCase):

    def setUp(self):
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def test_competitions_euro(self):
        competitions = sb.competitions()
        self.assertEqual(74, len(competitions))
        euro_2024 = competitions.iloc[68]
        self.assertEqual("UEFA Euro", euro_2024['competition_name'])
        self.assertEqual('2024', euro_2024['season_name'])
        self.assertEqual(55, euro_2024['competition_id'])
        self.assertEqual(282, euro_2024['season_id'])
        # print(competitions.sort_values(by='season_name', ascending=False))

    def test_competitions_with_360_frames(self):
        competitions = sb.competitions()
        self.assertEqual(74, len(competitions))
        filtered_competitions = competitions[(competitions['match_available_360'].notnull()) & (competitions['competition_international'] == True)]
        self.assertEqual(5, len(filtered_competitions))
        self.assertEqual(['FIFA World Cup',
                          'UEFA Euro',
                          'UEFA Euro',
                          "UEFA Women's Euro",
                          "Women's World Cup"], filtered_competitions['competition_name'].to_list())
        self.assertEqual(['2022',
                          '2024',
                          '2020',
                          "2022",
                          "2023"], filtered_competitions['season_name'].to_list())

    def test_matches(self):
        matches = sb.matches(55, 282)
        # print(matches)
        self.assertEqual(51, len(matches))
        team_name = 'Spain'
        matches_spain = matches[(matches['home_team'] == team_name) | (matches['away_team'] == team_name)]
        self.assertEqual(7, len(matches_spain))

    def test_matches_final(self):
        matches = sb.matches(55, 282).sort_values(by='match_date', ascending=False)
        self.assertEqual(51, len(matches))
        self.assertEqual(['match_id', 'match_date', 'kick_off', 'competition', 'season',
                          'home_team', 'away_team', 'home_score', 'away_score', 'match_status',
                          'match_status_360', 'last_updated', 'last_updated_360', 'match_week',
                          'competition_stage', 'stadium', 'referee', 'home_managers',
                          'away_managers', 'data_version', 'shot_fidelity_version',
                          'xy_fidelity_version'], matches.columns.to_list())

        final_match = matches.iloc[0]
        self.assertEqual(3943043, final_match['match_id'])
        self.assertEqual("Final", final_match['competition_stage'])
        self.assertEqual("2024-07-14", final_match['match_date'])
        self.assertEqual("SpainEngland", final_match['home_team'] + final_match['away_team'])
        self.assertEqual("21", str(final_match['home_score']) + str(final_match['away_score']))

    def test_events(self):
        events = sb.events(3943043)
        goals = events[events['shot_outcome'] == 'Goal']
        goals = goals.dropna(axis=1, how='all')
        print(goals)
        self.assertEqual(len(goals), 3)
        self.assertEqual(goals.iloc[0]["player"], "Nicholas Williams Arthuer")
        self.assertEqual(goals.iloc[1]["player"], "Cole Palmer")
        self.assertEqual(goals.iloc[2]["player"], "Mikel Oyarzabal Ugarte")

    def test_events_shots(self):
        events = sb.events(3943043)
        shots = events[events['type'] == 'Shot']
        self.assertEqual(len(shots), 25)
        self.assertEqual(len(shots[shots["team"] == "Spain"]), 16)
        self.assertEqual(len(shots[shots["team"] == "England"]), 9)

    def test_events_filter_shots(self):
        shots = sb.events(3943043, filters={"type": "Shot"})
        self.assertEqual(len(shots), 25)
        self.assertEqual(len(shots[shots["team"] == "Spain"]), 16)
        self.assertEqual(len(shots[shots["team"] == "England"]), 9)


class UtilsTests(unittest.TestCase):

    def test_get_competition_data(self):
        euro_2024 = utl.get_competition_data(55, 282)
        self.assertEqual("UEFA Euro", euro_2024['competition_name'])
        self.assertEqual('2024', euro_2024['season_name'])
        self.assertEqual(55, euro_2024['competition_id'])
        self.assertEqual(282, euro_2024['season_id'])

    def test_get_competition_info(self):
        competition, matches = get_competition_info(55, 282)

        self.assertEqual("UEFA Euro", competition['competition_name'])
        self.assertEqual("Europe", competition['country_name'])
        self.assertEqual("2024", competition['season_name'])

        self.assertEqual(51, len(matches))
        self.assertEqual(['match_id', 'match_date', 'home_team', 'away_team', 'score'], matches.columns.to_list())

    def test_get_events_type_counts(self):
        type_counts = get_events_type_counts(3938637)

        print(type_counts)
        self.assertEqual(27, len(type_counts))
        self.assertEqual(954, type_counts['Pass'])
        self.assertEqual([954, 919, 810, 263, 73, 54, 45, 44, 38, 33, 28, 21, 21, 18, 18, 16, 12, 10, 5, 4, 4, 2, 2, 2, 2, 2, 1], type_counts.values.tolist())
        self.assertEqual(
            ['Pass', 'Ball Receipt*', 'Carry', 'Pressure', 'Ball Recovery', 'Duel', 'Block', 'Clearance', 'Goal Keeper', 'Shot', 'Dribble', 'Dribbled Past',
             'Dispossessed', 'Foul Committed', 'Foul Won', 'Interception', 'Miscontrol', 'Substitution', 'Tactical Shift', 'Half Start', 'Half End',
             'Player On', '50/50', 'Starting XI', 'Player Off', 'Injury Stoppage', 'Error'], type_counts.keys().to_list())

    def test_get_events_type_counts_for_all_euro_matches(self):
        matches = sb.matches(55, 282)
        for match_id in matches['match_id'].to_list():
            type_counts = get_events_type_counts(match_id)
            self.assertLessEqual(len(type_counts), 33)

    def test_get_events_type(self):
        event_types = get_events_type_unique(3938637)
        print(event_types)
        self.assertEqual(len(event_types), 27)
        self.assertEqual(event_types,
                         {'Pass', 'Ball Receipt*', 'Carry', 'Pressure', 'Ball Recovery', 'Duel', 'Block', 'Clearance', 'Goal Keeper', 'Shot', 'Dribble',
                          'Dribbled Past',
                          'Dispossessed', 'Foul Committed', 'Foul Won', 'Interception', 'Miscontrol', 'Substitution', 'Tactical Shift', 'Half Start',
                          'Half End',
                          'Player On', '50/50', 'Starting XI', 'Player Off', 'Injury Stoppage', 'Error'})

    def test_get_events_type_comparison(self):
        type_counts_poland = get_events_type_unique(3938637)
        type_counts_other = get_events_type_unique(3930167)  # all the event types
        difference = type_counts_other.difference(type_counts_poland)
        self.assertEqual(difference, {'Referee Ball-Drop', 'Own Goal Against', 'Shield', 'Own Goal For', 'Offside', 'Bad Behaviour'})
        self.assertEqual(len(type_counts_other) - len(type_counts_poland), 6)
        self.assertEqual(len(difference), 6)

        union = type_counts_other.union(type_counts_poland)
        self.assertEqual(len(union), 33)

    def test_get_events_type_all_euro_matches_union(self):
        union = set()
        matches = sb.matches(55, 282)
        for match_id in matches['match_id'].to_list():
            union.update(get_events_type_unique(match_id))

        self.assertEqual(len(union), 33)
        self.assertEqual(union, {'Dispossessed', 'Dribbled Past', 'Referee Ball-Drop', 'Own Goal For', 'Half Start', 'Foul Committed', 'Error', 'Goal Keeper',
                                 'Starting XI', 'Ball Recovery', 'Dribble', 'Player Off', 'Foul Won', 'Carry', 'Bad Behaviour', 'Block', 'Interception',
                                 'Tactical Shift', 'Pressure', 'Player On', 'Half End', 'Injury Stoppage', 'Offside', 'Pass', 'Substitution', 'Ball Receipt*',
                                 'Shield', 'Miscontrol', 'Own Goal Against', 'Shot', '50/50', 'Clearance', 'Duel'})


class LineupsTests(unittest.TestCase):

    def test_unique_positions_matches(self):
        competitions = sb.competitions()
        for _, competition in competitions.iterrows():
            competition_id = competition['competition_id']
            season_id = competition['season_id']
            positions = _unique_positions_matches(competition_id, season_id)
            for pos in positions:
                self.assertIsNotNone(_get_position_coordinates(pos))
            self.assertGreaterEqual(25, len(positions))

    def test_unique_positions(self):
        positions = unique_positions(3942382)
        self.assertEqual(14, len(positions))
        self.assertEqual({'Center Attacking Midfield',
                          'Center Back',
                          'Center Forward',
                          'Goalkeeper',
                          'Left Back',
                          'Left Center Back',
                          'Left Defensive Midfield',
                          'Left Wing',
                          'Left Wing Back',
                          'Right Back',
                          'Right Center Back',
                          'Right Defensive Midfield',
                          'Right Wing',
                          'Right Wing Back'}, positions)

    def test_starting_lineups(self):
        lineups = starting_lineups(3942382)
        print(lineups)
        netherlands = lineups["Netherlands"]
        self.assertEqual(11, len(netherlands))
        self.assertEqual(['Center Forward',
                          'Left Back',
                          'Left Center Back',
                          'Right Center Back',
                          'Right Back',
                          'Right Wing',
                          'Right Defensive Midfield',
                          'Left Wing',
                          'Left Defensive Midfield',
                          'Goalkeeper',
                          'Center Attacking Midfield']
                         , netherlands['starting_position'].to_list())
        turkey = lineups["Turkey"]
        self.assertEqual(11, len(turkey))
        self.assertEqual(['Left Defensive Midfield',
                          'Right Defensive Midfield',
                          'Right Wing Back',
                          'Right Center Back',
                          'Goalkeeper',
                          'Left Wing Back',
                          'Left Center Back',
                          'Right Wing',
                          'Center Back',
                          'Center Forward',
                          'Left Wing']
                         , turkey['starting_position'].to_list())

    def test_display_starting_lineups(self):
        display_starting_lineups(3943043, "Final match")
        self.assertTrue(True)

    def test_display_starting_lineup(self):
        positions = starting_lineups(3943043)
        for key, value in positions.items():
            display_starting_lineup(key, value)
        self.assertEqual({"Spain", "England"}, positions.keys(), "Netherlands")

    def test_extract_match_title(self):
        matches = sb.matches(55, 282)
        title = extract_match_title(matches.iloc[0])
        self.assertEqual("Europe - UEFA Euro - 2024\nSemi-finals\nNetherlands 1:2 England\n2024-07-10, 22:00 Signal-Iduna-Park\nReferee: Felix Zwayer", title)

    def test_display_competition_lineups(self):
        # display_competition_lineups()
        self.assertTrue(True)

    def test_display_match_lineups(self):
        display_match_lineups(3943043, 55, 282)
        self.assertTrue(True)

    def test_display_match_lineups_no_title(self):
        display_match_lineups(3943043)
        self.assertTrue(True)

    def test_display_match_lineups_ucl_final_2014(self):
        display_match_lineups(18242)
        self.assertTrue(True)


class FramesTests(unittest.TestCase):
    match_id = 3938637  # Poland - Netherlands
    first_3_event_ids = ["57b3cd29-6810-47e7-a7c2-2baf15c4fd6b", "a161c7af-83ad-4d4d-8690-7e37687558ad", "8e1d7296-b2ab-4b1a-b22a-a0885454bda4"]

    def test_plot_polygon(self):
        frames = sb.frames(self.match_id)
        frames = frames[frames['id'] == "7f3a8532-8312-41f5-9380-2b3bad74ace5"]
        frame = frames.iloc[0]
        plot_polygon(frame['visible_area'])
        plt.show()
        self.assertEqual(18, len(frames))

    def test_plot_frame_group(self):
        frames = sb.frames(self.match_id)
        grouped = frames.groupby('id')
        frame_group = grouped.get_group("57b3cd29-6810-47e7-a7c2-2baf15c4fd6b")  # Kick of, Pass
        plot_frame_group(frame_group)
        plt.show()
        self.assertEqual(20, len(frame_group))

    def test_plot_frame_group_first_3_events(self):
        frames = sb.frames(self.match_id)
        grouped = frames.groupby('id')
        for frame_id in self.first_3_event_ids:
            frame_group = grouped.get_group(frame_id)
            plot_frame_group(frame_group)
            plt.show()
        self.assertEqual(2936, len(grouped))


class MatchesTests(unittest.TestCase):

    def test_display_shots(self):
        m.display_shots(3943043)  ## final
        self.assertTrue(True)

    def test_plot_shots(self):
        shots = sb.events(3943043, filters={"type": "Shot"})
        m.plot_shots(shots, "Shots")
        self.assertTrue(True)

    def test_plot_shots_by_team(self):
        m.plot_shots_by_team(3943043)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

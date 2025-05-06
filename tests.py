import unittest

from matplotlib import pyplot as plt

import src.utils as utl
from src.frames import plot_polygon, plot_frame_group
from src.lineups.lineups import starting_lineups, unique_positions, _unique_positions_matches
from src.lineups.matches import extract_match_title, display_match_lineups
from src.lineups.pitch import _get_position_coordinates, display_starting_lineup, display_starting_lineups
from statsbombpy import sb


class StatsbombPyTests(unittest.TestCase):

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
        self.assertEqual(51, len(matches))
        team_name = 'Spain'
        matches_spain = matches[(matches['home_team'] == team_name) | (matches['away_team'] == team_name)]
        self.assertEqual(7, len(matches_spain))


class UtilsTests(unittest.TestCase):

    def test_get_competition_data(self):
        competitions = utl.get_competition_data(55, 282)
        self.assertEqual(1, len(competitions))
        euro_2024 = competitions.iloc[0]
        self.assertEqual("UEFA Euro", euro_2024['competition_name'])
        self.assertEqual('2024', euro_2024['season_name'])
        self.assertEqual(55, euro_2024['competition_id'])
        self.assertEqual(282, euro_2024['season_id'])

    def test_matches(self):
        matches = sb.matches(55, 282)
        print(matches)
        print(matches.columns)
        # print(competitions.sort_values(by='season_name', ascending=False))


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


if __name__ == '__main__':
    unittest.main()

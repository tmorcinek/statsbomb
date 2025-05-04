import unittest

from matplotlib import pyplot as plt

from src.frames import plot_polygon, plot_frame_group
from src.lineups.lineups import starting_lineups, unique_positions, _unique_positions_matches
from src.lineups.pitch import _get_position_coordinates
from statsbombpy import sb


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


class FramesTests(unittest.TestCase):
    match_id = 3938637  # Poland - Netherlands
    kick_of_id = "57b3cd29-6810-47e7-a7c2-2baf15c4fd6b"  # Kick of, Pass
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
        frame_group = grouped.get_group(self.kick_of_id)
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

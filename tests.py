import unittest

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


if __name__ == '__main__':
    unittest.main()

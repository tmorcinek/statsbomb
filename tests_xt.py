import unittest

import pandas as pd

import src.events.data as dt
import src.xT.expected_threat as xt


class ExpectedThreatTests(unittest.TestCase):

    def setUp(self):
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def test_get_zone(self):
        zone = xt.get_zone(0, 0)
        self.assertEqual((0, 0), zone)

        zone = xt.get_zone(120, 0)
        self.assertEqual((15, 0), zone)

        zone = xt.get_zone(120, 80)
        self.assertEqual((15, 11), zone)

    def test_get_zone_shots(self):
        shots = dt.shots(3943043)
        spain_shots = shots[shots["team"] == "Spain"]
        self.assertEqual(16, len(spain_shots))

        location_ = spain_shots.iloc[0]['location']
        self.assertEqual([115.6, 28.4], location_)
        self.assertEqual((15, 4), xt.get_zone(*location_))

        location_ = spain_shots.iloc[1]['location']
        self.assertEqual([112.9, 36.2], location_)
        self.assertEqual((15, 5), xt.get_zone(*location_))

        location_ = spain_shots.iloc[2]['location']
        self.assertEqual([101.2, 49.8], location_)
        self.assertEqual((13, 7), xt.get_zone(*location_))

        location_ = spain_shots.iloc[3]['location']
        self.assertEqual([95.0, 31.2], location_)
        self.assertEqual((12, 4), xt.get_zone(*location_))

    def test_get_competition_goals(self):
        all_goals = xt.get_competition_goals()

        self.assertEqual(117, len(all_goals))

    def test_get_competition_shots(self):
        all_shots = xt.get_competition_shots()

        self.assertEqual(1340, len(all_shots))

    def test_get_competition_shots_with_own_goals(self):
        all_shots = xt.get_competition_shots(own_goals_included=True)

        self.assertEqual(1350, len(all_shots))

    def test_get_competition_passes(self):
        all_passes = xt.get_competition_passes()

        self.assertEqual(53890, len(all_passes))


if __name__ == '__main__':
    unittest.main()

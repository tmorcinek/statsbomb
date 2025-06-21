import unittest

import pandas as pd

import src.xT.expected_threat as xt
import src.events.data as dt
from statsbombpy import sb


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
        print(shots.dropna(axis=1, how="all"))
        spain_shots = shots[shots["team"] == "Spain"]

        self.assertEqual(16, len(spain_shots))

    def test_get_competition_shots(self):
        all_goals = xt.get_competition_goals()

        self.assertEqual(117, len(all_goals))


if __name__ == '__main__':
    unittest.main()

import matplotlib.pyplot as plt

from utils import *

if __name__ == '__main__':
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    json = '../open-data/data/events/3938637.json'
    # display_shots(json)
    # print_events(json)
    # print_competitions()
    # print_competition(55, 282)
    print_match(3938637)
    # print_competition_bayer()
    # df = competition_df(9, 281)
    # print(df)
    # plt.show()

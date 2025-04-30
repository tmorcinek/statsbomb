import matplotlib.pyplot as plt
import pandas as pd
import utils as utl
import match as m

if __name__ == '__main__':
    # pd.set_option('display.width', 1000)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)

    json = '../open-data/data/events/3938637.json'
    # utl.display_shots(json)
    # print_events(json)
    # utl.print_competitions()
    # utl.print_competition(55, 282)
    utl.print_match(3938637)
    # m.print_match(3938637)
    m.display_shots(json)
    # print_competition_bayer()
    # df = competition_df(9, 281)
    # print(df)
    plt.show()

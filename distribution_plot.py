import os
import plotly.figure_factory as ff
import pandas as pd


if __name__ == '__main__':

    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)
    users: list = [df['n_users'].tolist()]

    fig = ff.create_distplot(users, ['Users'], bin_size=[5])
    fig.update_layout(xaxis_type="log")
    fig.show()

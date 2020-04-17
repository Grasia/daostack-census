import os
import plotly.express as px
import pandas as pd


if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    fig = px.histogram(df, 'n_users', nbins=50, labels={'n_users':'Users'})
    fig.show()

    fig = px.histogram(df, 'n_proposals', nbins=50, labels={'n_proposals':'Proposals'})
    fig.show()

    fig = px.histogram(df, 'n_votes', nbins=100, labels={'n_votes':'Votes'})
    fig.show()

    fig = px.histogram(df, 'n_stakes', nbins=20, labels={'n_stakes':'Stakes'})
    fig.show()

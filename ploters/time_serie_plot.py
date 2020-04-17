import os
import pandas as pd
import plotly.graph_objects as go

DATE_FORMAT: str = '%b, %Y'
DARK_BLUE: str = '#2471a3'
LIGHT_BLUE: str = '#d4e6f1'


def update_layout(df: pd.DataFrame, fig: go.Figure, title: str) -> None:
    fig.update_layout(
        xaxis={
            'tickvals': df['date'],
            'tickformat': DATE_FORMAT,
            'tickangle': 45,
            'type': 'date',
        },
        yaxis={
            'title': title,
        },
        plot_bgcolor="white",
    )


def plot(df: pd.DataFrame, title: str) -> None:
    colors: list = [LIGHT_BLUE] * len(df.index)
    colors[-1] = DARK_BLUE

    fig = go.Figure(data=[
        go.Bar(
            x=df['date'], 
            y=df['actives'],
            marker_color=colors)
    ])

    update_layout(df, fig, title)
    fig.show()


def process_df(df: pd.DataFrame, key_id: str) -> pd.DataFrame:
    dff = df
    dff = dff.groupby([key_id, 'date']).size().reset_index(name='nActions')

    # before remove nActions use it if you want to filter more than one action
    dff = dff.drop(columns=['nActions'])
    dff = dff.groupby(['date']).size().reset_index(name='actives')

    return dff


if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'activity_serie.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # let's transform the date
    df['unixDate'] = pd.to_datetime(df['unixDate'], unit='s').dt.date
    df = df.rename(columns={'unixDate': 'date'})

    # transform to monthly date
    df['date'] = df['date'].apply(lambda d: d.replace(day=1))

    # active DAOs
    dff = df.drop(columns=['daoName', 'actionType', 'userId'])
    dff = process_df(dff, 'daoId')
    plot(dff, 'Number of active DAOs')

    # active users
    dff = df.drop(columns=['daoName', 'daoId', 'actionType'])
    dff = process_df(dff, 'userId')
    plot(dff, 'Number of active users')

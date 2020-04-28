import os
import pandas as pd
import plotly.graph_objects as go

DATE_FORMAT: str = '%b, %Y'
DARK_BLUE: str = '#2471a3'
LIGHT_BLUE: str = '#d4e6f1'
GRID_COLOR: str = '#B0BEC5'


def update_layout(df: pd.DataFrame, fig: go.Figure) -> None:
    fig.update_layout(
        xaxis={
            'tickvals': df['date'],
            'tickformat': DATE_FORMAT,
            'tickangle': 45,
            'type': 'date',
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
        },
        yaxis={
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': GRID_COLOR,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
        },
        plot_bgcolor="white",
    )


def plot(df: pd.DataFrame, y_key: str) -> None:
    colors: list = [DARK_BLUE] * len(df.index)
    colors[-1] = LIGHT_BLUE

    fig = go.Figure(data=[
        go.Scatter(
            x=df['date'], 
            y=df[y_key],
            marker_color=colors,
            marker_size=12,
            marker_line_width=2,
            line_color=DARK_BLUE)
    ])

    update_layout(df, fig)
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
    plot(dff, 'actives')

    # active users
    dff = df.drop(columns=['daoName', 'daoId', 'actionType'])
    dff = process_df(dff, 'userId')
    plot(dff, 'actives')

    # new proposals
    dff = df[df['actionType'] == 'proposal']
    dff = dff.drop(columns=['daoName', 'daoId', 'actionType', 'userId'])
    dff = dff.groupby(['date']).size().reset_index(name='nProposals')
    plot(dff, 'nProposals')

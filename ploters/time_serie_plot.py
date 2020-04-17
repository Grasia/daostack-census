import os
import pandas as pd
import plotly.graph_objects as go

DATE_FORMAT: str = '%b, %Y'
DARK_BLUE: str = '#2471a3'
LIGHT_BLUE: str = '#d4e6f1'

if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'activity_serie.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # let's transform the date
    df['unixDate'] = pd.to_datetime(df['unixDate'], unit='s').dt.date
    df = df.rename(columns={'unixDate': 'date'})

    # transform to monthly date
    df['date'] = df['date'].apply(lambda d: d.replace(day=1))

    # active DAO means at least one action per month
    dff = df.drop(columns=['daoName', 'actionType', 'userId'])
    dff = dff.groupby(['daoId', 'date']).size().reset_index(name='nActions')

    # before remove nActions use it if you want to filter more than one action
    dff = dff.drop(columns=['nActions'])
    dff = dff.groupby(['date']).size().reset_index(name='activeDaos')

    colors: list = [LIGHT_BLUE] * len(dff.index)
    colors[-1] = DARK_BLUE

    fig = go.Figure(data=[
        go.Bar(
            x=dff['date'].tolist(), 
            y=dff['activeDaos'].tolist(),
            marker_color=colors)
    ])

    fig.update_layout(
        xaxis={
            'tickvals': dff['date'],
            'tickformat': DATE_FORMAT,
            'tickangle': 45,
            'type': 'date',
        },
        yaxis={
            'title': 'Number of active DAOs',
        },
        plot_bgcolor="white",
    )

    fig.show()

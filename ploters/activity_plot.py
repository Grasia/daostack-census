import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

LIGHT_BLUE: str = '#d4e6f1'
GRID_COLOR: str = '#B0BEC5'

def transform_to_monthly_date(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff['date'] = pd.to_datetime(dff['date'], unit='s')
    dff['date'] = dff['date'].apply(lambda d: d.replace(day=1))
    return dff


def get_months_between(date1: datetime, date2: datetime) -> int:
    start: datetime = date1 if date1 < date2 else date2
    end: datetime = date1 if date1 > date2 else date2

    return (end.year - start.year) * 12 + (end.month - start.month) + 1


def calculate_month_activity() -> pd.DataFrame:
    # get now date
    now_date = datetime.now().replace(day=1)

    # load DAOs data
    filename: str = os.path.join('datawarehouse', 'census.csv')
    daos: pd.DataFrame = pd.read_csv(filename, header=0)
    daos = daos.rename(columns={'birth': 'date'})
    daos = transform_to_monthly_date(daos)

    # remove unused cols
    daos = daos.drop(columns=['nUsers', 'nProposals', 'nVotes', 'nStakes',
        'ETH', 'GEN', 'otherTokens'])

    # let's add month between now date and DAO's birth date
    daos['monthLife'] = 0
    for i, r in daos.iterrows():
        daos.loc[i, 'monthLife'] = get_months_between(now_date, r['date'])

    # load activity registry
    filename: str = os.path.join('datawarehouse', 'activity_serie.csv')
    activity: pd.DataFrame = pd.read_csv(filename, header=0)
    activity = activity.rename(columns={'unixDate': 'date'})
    activity = transform_to_monthly_date(activity)
    
    # remove unused cols
    activity = activity.drop(columns=['actionType', 'userId', 'daoName'])

    # calculate activity months by DAO
    activity['date'] = activity['date'].dt.date
    activity = activity.groupby(['daoId', 'date']).size().reset_index()
    activity = activity.groupby(['daoId']).size().reset_index(name='activityMonths')
    
    # add activity months to DAOs
    daos['activityMonths'] = 0
    for i, row in daos.iterrows():
        r = activity[activity['daoId'] == row['id']]
        if not r.empty:
            daos.loc[i, 'activityMonths'] = r.iloc[0]['activityMonths']

    return daos


if __name__ == '__main__':
    daos = calculate_month_activity()
    # sort by activityMonths
    daos = daos.sort_values(by=['activityMonths'])

    # plot result
    fig = go.Figure(
        data=[
            go.Bar(
                x=daos['name'], 
                y=daos['activityMonths'], 
                marker_color=LIGHT_BLUE,
                name='Real month activity'),
            go.Scatter(
                x=daos['name'], 
                y=daos['monthLife'],
                name='Max months which can get activity',
                marker_color='black', 
                mode='markers',
                marker_symbol='x-thin-open')
        ])

    fig.update_layout(
        xaxis={
            'tickangle': 45,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': GRID_COLOR,
            'tickfont': {'size': 14},
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
            'tickfont': {'size': 14},
        },
        plot_bgcolor="white",
        legend={'orientation': 'h', 'x': 0, 'y': 1.2}
    )

    fig.show()

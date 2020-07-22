import os
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict

BLUE: str = '#2471a3'
RED: str = '#C62828'
GRID_COLOR: str = '#B0BEC5'

def get_daos() -> List[str]:
    filename: str = os.path.join('datawarehouse', 'census.csv')
    return pd.read_csv(filename, header=0)


def get_proposals() -> pd.DataFrame:
    filename: str = os.path.join('datawarehouse', 'proposals.csv')
    return pd.read_csv(filename, header=0)


def calculate_ratio(tp: int, tn: int, fp: int, fn: int) -> float:
    numerator: int = tp + tn
    denominator: int = tp + tn + fp + fn

    return round(numerator / denominator, 2) if denominator > 0 else None


def get_validation_value(df: pd.DataFrame, valid: str) -> int:
    """ 
    True positives = boost and pass
    True negatives = not boost and not pass
    False positives = boost and not pass
    False negatives = not boost and pass

    Parameters:
        * df = data frame to filter
        * valid = must be 'tp', 'tn', 'fp', 'fn' in other case return true 
                    positive by default.
    Return:
        The number of 'valid' parameter.
    """
    boosted: bool = True
    approved: bool = True

    if valid == 'tn':
        boosted = False
        approved = False
    elif valid == 'fp':
        approved = False
    elif valid == 'fn':
        boosted = False

    dff = df[df['hasPassed'] == approved]
    if boosted:
        dff = dff[dff.boostedAt.notnull()]
    else:
        dff = dff[~dff.boostedAt.notnull()]

    return len(dff.index)


def get_prediction_accuracy(ids: List[str], proposals: pd.DataFrame) -> Dict[str, float]:
    accuracy: Dict[str, float] = dict()

    for d_id in ids:
        df: pd.DataFrame = proposals[proposals['daoId'] == d_id]

        tp: int = get_validation_value(df=df, valid='tp')
        tn: int = get_validation_value(df=df, valid='tn')
        fp: int = get_validation_value(df=df, valid='fp')
        fn: int = get_validation_value(df=df, valid='fn')

        accuracy[d_id] = calculate_ratio(tp=tp, tn=tn, fp=fp, fn=fn)

    return accuracy


def add_dict_param(df: pd.DataFrame, param: Dict, name: str) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff[name] = 0

    for i, row in dff.iterrows():
        dff.loc[i, name] = param[row['id']]

    return dff


def update_layout(fig: go.Figure) -> None:
    fig.update_layout(
        xaxis={
            'tickangle': 45,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True,
            'linewidth': 2, 
            'linecolor': 'black',
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
            'nticks': 5,
            'dtick': 0.2,
            'tickfont': {'size': 14},
        },
        plot_bgcolor="white",
        #showlegend=False,
        legend={'orientation': 'h', 'x': 0, 'y': 1.2},
    )


if __name__ == '__main__':
    daos: pd.DataFrame = get_daos()
    proposals: pd.DataFrame = get_proposals()
    accuracy: Dict[str, float] = get_prediction_accuracy(ids=daos['id'].tolist(), proposals=proposals)

    # add accuracy as new parameter
    daos = add_dict_param(df=daos, param=accuracy, name='accuracy')

    # sort by number of users
    daos = daos.sort_values(by=['nUsers'])

    # median of number users
    median: float = daos['nUsers'].quantile(.5)

    # add colours by number of proposals
    daos['color'] = '#BDBDBD'
    for i, row in daos.iterrows():
        if 0 < row['nProposals'] < 11: 
            daos.loc[i, 'color'] = '#E1BEE7'
        elif 10 < row['nProposals'] < 26: 
            daos.loc[i, 'color'] = '#BA68C8'
        elif 25 < row['nProposals'] < 51: 
            daos.loc[i, 'color'] = '#8E24AA'
        elif 50 < row['nProposals'] < 101: 
            daos.loc[i, 'color'] = '#4A148C'
        elif 100 < row['nProposals']: 
            daos.loc[i, 'color'] = '#C2185B'

    # filters
    daos = daos[daos['name'] != 'BuffiDAO']
    daos = daos[daos['name'] != 'Fortmatic DAO']

    # plot
    fig: go.Figure = go.Figure()

    dff = daos[daos['nUsers'] <= median]
    fig.add_trace(go.Scatter(
        x=dff['name'], 
        y=dff['accuracy'],
        mode='markers',
        marker=dict(
            size=12,
            color=dff['color']
        ),
        showlegend=False))

    # add vertical separation
    fig.add_shape(
        dict(
            type="line",
            x0="",
            y0=0,
            x1="",
            y1=1,
            line=dict(
                color="black",
                width=3,
                dash="dashdot",
            )
        )
    )

    dff = daos[daos['nUsers'] > median]
    fig.add_trace(go.Scatter(
        x=dff['name'], 
        y=dff['accuracy'],
        mode='markers',
        marker=dict(
            size=12,
            color=dff['color']
        ),
        showlegend=False))

    # add empty elements for the legend
    fig.add_trace(go.Scatter(
        x=[None], 
        y=[None],
        name='0 > Proposals < 11',
        mode='markers',
        marker=dict(
            size=10,
            color='#E1BEE7',
        )))

    fig.add_trace(go.Scatter(
        x=[None], 
        y=[None],
        name='10 > Proposals < 26',
        mode='markers',
        marker=dict(
            size=10,
            color='#BA68C8',
        )))

    fig.add_trace(go.Scatter(
        x=[None], 
        y=[None],
        name='25 > Proposals < 51',
        mode='markers',
        marker=dict(
            size=10,
            color='#8E24AA',
        )))

    fig.add_trace(go.Scatter(
        x=[None], 
        y=[None],
        name='50 > Proposals < 101',
        mode='markers',
        marker=dict(
            size=10,
            color='#4A148C',
        )))

    fig.add_trace(go.Scatter(
        x=[None], 
        y=[None],
        name='100 > Proposals',
        mode='markers',
        marker=dict(
            size=10,
            color='#C2185B',
        )))

    update_layout(fig=fig)
    fig.show()

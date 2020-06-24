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

    # add color by number of users
    daos['color'] = ''
    median: float = daos['nUsers'].quantile(.5)

    for i, row in daos.iterrows():
        daos.loc[i, 'color'] = BLUE if row['nUsers'] < median else RED

    # plot
    fig: go.Figure = go.Figure()

    dff = daos[daos['color'] == BLUE]
    fig.add_trace(go.Scatter(
        x=dff['name'], 
        y=dff['accuracy'],
        mode='markers',
        marker_color=dff['color'],
        marker_size=12,
        marker_line_width=2,
        name='Group A'))

    dff = daos[daos['color'] == RED]
    fig.add_trace(go.Scatter(
        x=dff['name'], 
        y=dff['accuracy'],
        mode='markers',
        marker_color=dff['color'],
        marker_size=12,
        marker_line_width=2,
        name='Group B'))

    update_layout(fig=fig)
    fig.show()

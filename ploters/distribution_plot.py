import os
import plotly.graph_objects as go
import pandas as pd

GRID_COLOR: str = '#B0BEC5'
BLUE: str = '#2471a3'

def update_layout(fig: go.Figure) -> None:
    fig.update_layout(
        xaxis={
            'tick0': 0,
            'dtick': 20,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'tickangle': 45,
            'tickfont': {'size': 14},
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
            'tickfont': {'size': 14},
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
        },
        plot_bgcolor="white",
    )


if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # users
    fig = go.Figure(data=[go.Histogram(
        x=df['n_users'].tolist(), 
        xbins={'size': 10.0},
        marker_color=BLUE,
        )])

    update_layout(fig=fig)
    fig.show()

    # proposals
    fig = go.Figure(data=[go.Histogram(
        x=df['n_proposals'].tolist(), 
        xbins={'size': 10.0},
        marker_color=BLUE,
        )])

    update_layout(fig=fig)
    fig.show()

    # votes
    fig = go.Figure(data=[go.Histogram(
        x=df['n_votes'].tolist(), 
        xbins={'size': 10.0},
        marker_color=BLUE,
        )])

    update_layout(fig=fig)
    fig.show()

    # stakes
    fig = go.Figure(data=[go.Histogram(
        x=df['n_stakes'].tolist(), 
        xbins={'size': 10.0},
        marker_color=BLUE,
        )])

    update_layout(fig=fig)
    fig.show()

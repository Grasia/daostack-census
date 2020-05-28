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
            'tick0': 0,
            'dtick': 1,
        },
        plot_bgcolor="white",
    )


if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # users
    fig = go.Figure(data=[go.Histogram(
        x=df['nUsers'].tolist(), 
        xbins={'size': 10.0, 'start': 1.0},
        marker_color=BLUE,
        )])

    fig.add_trace(go.Scatter(
        x=[0, 0], 
        y=[0, len(df[df['nUsers'] == 0])],
        line=dict(color='firebrick', width=4)
        ))

    update_layout(fig=fig)
    fig.update_layout(xaxis_title_text='Number of users', yaxis_title_text='Number of DAOs')
    fig.show()

    # proposals
    fig = go.Figure(data=[go.Histogram(
        x=df['nProposals'].tolist(), 
        xbins={'size': 10.0, 'start': 1.0},
        marker_color=BLUE,
        )])

    fig.add_trace(go.Scatter(
        x=[0, 0], 
        y=[0, len(df[df['nProposals'] == 0])],
        line=dict(color='firebrick', width=4)
        ))

    update_layout(fig=fig)
    fig.update_layout(xaxis_title_text='Number of proposals', yaxis_title_text='Number of DAOs')
    fig.show()

    # votes
    fig = go.Figure(data=[go.Histogram(
        x=df['nVotes'].tolist(), 
        xbins={'size': 10.0, 'start': 1.0},
        marker_color=BLUE,
        )])

    fig.add_trace(go.Scatter(
        x=[0, 0], 
        y=[0, len(df[df['nVotes'] == 0])],
        line=dict(color='firebrick', width=4)
        ))

    update_layout(fig=fig)
    fig.update_layout(xaxis_title_text='Number of votes', yaxis_title_text='Number of DAOs')
    fig.show()

    # stakes
    fig = go.Figure(data=[go.Histogram(
        x=df['nStakes'].tolist(), 
        xbins={'size': 10.0, 'start': 1.0},
        marker_color=BLUE,
        )])

    fig.add_trace(go.Scatter(
        x=[0, 0], 
        y=[0, len(df[df['nStakes'] == 0])],
        line=dict(color='firebrick', width=4)
        ))

    update_layout(fig=fig)
    fig.update_layout(xaxis_title_text='Number of stakes', yaxis_title_text='Number of DAOs')
    fig.show()

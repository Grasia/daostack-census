import os
import pandas as pd
import plotly.graph_objects as go

GRID_COLOR: str = '#B0BEC5'

if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # calculate total budget
    df['budget'] = df['ETH'] + df['GEN'] + df['otherTokens']
    df = df.sort_values(by=['budget'])

    # filter DAOs up to 1$
    df = df[df['budget'] >= 1]

    # budget stacked bar
    fig = go.Figure(data=[
        go.Bar(name='GEN', x=df['name'], y=df['GEN'], ),
        go.Bar(name='ETH', x=df['name'], y=df['ETH']),
        go.Bar(name='Other criptos', x=df['name'], y=df['otherTokens'])
    ])

    # Change layout
    fig.update_layout(
        barmode='stack',
        xaxis={
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
            'tick0': 0,
            'dtick': 1000,
            'ticksuffix': '$',
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
        legend=dict(
            x=0.01,
            y=0.98,
            traceorder="normal",
            font=dict(
                size=12,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=1
    ))

    fig.show()

    # Show stats
    eth = sum(df['ETH'].tolist())
    gen = sum(df['GEN'].tolist())
    others = sum(df['otherTokens'].tolist())
    total = eth + gen + others

    print(
        'Stats: \n' +
        f'Total funds = {round(total, 2)}$\n' +
        f'ETH = {round(eth, 2)}$ ~> {round(eth/total*100, 2)}%\n' +  
        f'GEN = {round(gen, 2)}$ ~> {round(gen/total*100, 2)}%\n' +
        f'Other criptos = {round(others, 2)} ~> {round(others/total*100, 2)}%')

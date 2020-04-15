import os
import pandas as pd
import plotly.graph_objects as go

if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # calculate total holdings
    df['holdings'] = df['ETH'] + df['GEN'] + df['otherTokens']
    df = df.sort_values(by=['holdings'])

    # holdings stacked bar
    fig = go.Figure(data=[
        go.Bar(name='ETH (USD)', x=df['name'], y=df['ETH']),
        go.Bar(name='GEN (USD)', x=df['name'], y=df['GEN']),
        go.Bar(name='Other criptos (USD)', x=df['name'], y=df['otherTokens'])
    ])

    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.show()

    eth = sum(df['ETH'].tolist())
    gen = sum(df['GEN'].tolist())
    others = sum(df['otherTokens'].tolist())
    total = eth + gen + others

    print(f'Stats: \n  ETH = {round(eth/total*100, 2)}%\n  GEN = \
{round(gen/total*100, 2)}%\n  Others = {round(others/total*100, 2)}%')

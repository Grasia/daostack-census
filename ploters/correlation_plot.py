import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import plotly.graph_objects as go

PLOT_COLOR: str = '#03A9F4'

if __name__ == '__main__':
    filename: str = os.path.join('datawarehouse', 'census.csv')
    df: pd.DataFrame = pd.read_csv(filename, header=0)

    # calculate total holdings
    df['holdings'] = df['ETH'] + df['GEN'] + df['otherTokens']

    sns.set(style="white", color_codes=True)

    # users vs proposals
    j = sns.jointplot(
        x=df["nUsers"], 
        y=df["nProposals"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)

    j.annotate(stats.pearsonr)

    # users vs votes
    j = sns.jointplot(
        x=df["nUsers"], 
        y=df["nVotes"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)
        
    j.annotate(stats.pearsonr)

    # users vs stakes
    j = sns.jointplot(
        x=df["nUsers"], 
        y=df["nStakes"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)
        
    j.annotate(stats.pearsonr)

    # users vs holdings
    j = sns.jointplot(
    x=df["nUsers"], 
    y=df["holdings"], 
    kind='scatter', 
    s=100, 
    color=PLOT_COLOR, 
    edgecolor='black', 
    linewidth=0.7,
    alpha=0.5)

    j.annotate(stats.pearsonr)

    plt.show()

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
from typing import List
import math

PLOT_COLOR: str = '#03A9F4'


def fill_ids(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = df1

    for i, row in df2.iterrows():
        r = df[df['id'] == row['id']]
        if r.empty:
            serie: pd.Series = pd.Series([row['id'], row['name'], 0], index=df.columns)
            df = df.append(serie, ignore_index=True)

    return df


def join_df_by_id(df1: pd.DataFrame, df2: pd.DataFrame, keys: List[str])\
-> pd.DataFrame:

    df: pd.DataFrame = df1
    # initialization
    for k in keys:
        df[k] = 0

    for i, row in df.iterrows():
        try:
            r = df2[df2['id'] == row['id']]
            for k in keys:
                df.loc[i, k] = r.iloc[0][k]
        except:
            pass

    return df


if __name__ == '__main__':
    # load daos stats
    filename: str = os.path.join('datawarehouse', 'census.csv')
    daos: pd.DataFrame = pd.read_csv(filename, header=0)

    # load proposals
    filename: str = os.path.join('datawarehouse', 'proposals.csv')
    props: pd.DataFrame = pd.read_csv(filename, header=0)
    props = props.rename(columns={'daoId': 'id'})

    # add some stats
    df = props.groupby(['id', 'daoName']).size().reset_index(name='nProposals')
    df = fill_ids(df, daos)
    df = join_df_by_id(df1=df, df2=daos, keys=['nUsers'])

    # add boost stats
    dff = props[props['boostedAt'].notnull()]
    dff = dff.groupby(['id']).size().reset_index(name='nBoost')
    df = join_df_by_id(df1=df, df2=dff, keys=['nBoost'])
    df['boostPercentage'] = None

    for i, row in df.iterrows():
        #df.loc[i, 'nUsers'] = math.log1p(row['nUsers'])
        if row['nProposals'] > 0:
            df.loc[i, 'boostPercentage'] = row['nBoost'] / row['nProposals'] * 100

    # # filter daos
    # df = df[df['daoName'] != 'Kyber DAO Exp#2']
    # df = df[df['daoName'] != 'Genesis Alpha']
    # df = df[df['daoName'] != 'dxDAO']

    
    sns.set(style="white", color_codes=True)
    # users vs boostPercentage
    j = sns.jointplot(
        x=df["nUsers"], 
        y=df["boostPercentage"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)

    j.annotate(stats.pearsonr)

    plt.show()

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import plotly.graph_objects as go
from typing import List
import math

from activity_plot import calculate_month_activity

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


def calculate_boost_data() -> pd.DataFrame:
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
    df = join_df_by_id(df1=df, df2=daos, keys=['nUsers', 'nVotes', 'nStakes'])

    # add boost stats
    dff = props[props['boostedAt'].notnull()]
    dff = dff.groupby(['id']).size().reset_index(name='nBoost')
    df = join_df_by_id(df1=df, df2=dff, keys=['nBoost'])
    df['boostPercentage'] = None

    # activity = stakes + votes + proposals
    df['activity'] = 0

    # calculate new metrics
    for i, row in df.iterrows():
        df.loc[i, 'activity'] = row['nStakes'] + row['nVotes'] + row['nProposals'] 
        if row['nProposals'] > 0:
            df.loc[i, 'boostPercentage'] = row['nBoost'] / row['nProposals'] * 100

    return df


def calculate_activity_ratio(df: pd.DataFrame) -> pd.DataFrame:
    if not 'activityMonths' in df.columns and 'monthLife' in df.columns:
        return df

    dff: pd.DataFrame = df
    dff['activityPercentage'] = 0

    for i, row in dff.iterrows():
        if row['monthLife'] > 0:
            dff.loc[i, 'activityPercentage'] = row['activityMonths'] / row['monthLife'] * 100

    return dff


if __name__ == '__main__':
    df: pd.DataFrame = calculate_boost_data()
    df1: pd.DataFrame = calculate_month_activity()

    df = join_df_by_id(df1=df, df2=df1, keys=['activityMonths', 'monthLife'])
    df = calculate_activity_ratio(df)

    # filters
    # df = df[df['daoName'] != 'Kyber DAO Exp#2']
    # df = df[df['daoName'] != 'Genesis Alpha']
    # df = df[df['daoName'] != 'dxDAO']
    # df = df[df['activityPercentage'] > 50]
    print(df)
    
    sns.set(style="white", color_codes=True)
    j = sns.jointplot(
        x=df["activityPercentage"], 
        y=df["boostPercentage"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)

    j.annotate(stats.spearmanr)

    plt.show()

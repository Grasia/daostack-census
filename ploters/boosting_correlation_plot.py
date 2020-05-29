import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
from typing import List

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

    # add proposal result
    dff = props[props['hasPassed'] == True]
    dff = dff.groupby(['id']).size().reset_index(name='nPropAccepted')
    df = join_df_by_id(df1=df, df2=dff, keys=['nPropAccepted'])
    dff = props[props['hasPassed'] == False]
    dff = dff.groupby(['id']).size().reset_index(name='nPropRejected')
    df = join_df_by_id(df1=df, df2=dff, keys=['nPropRejected'])
    df['acceptedPercentage'] = None
    df['rejectedPercentage'] = None

    # add boost stats
    dff = props[props['boostedAt'].notnull()]
    dff = dff.groupby(['id']).size().reset_index(name='nBoost')
    df = join_df_by_id(df1=df, df2=dff, keys=['nBoost'])
    df['boostPercentage'] = None

    # stakePer = nStakes / nProposals * 100
    dff = props[props['differentStakers'] > 0]
    dff = dff.groupby(['id']).size().reset_index(name='nPropStaked')
    df = join_df_by_id(df1=df, df2=dff, keys=['nPropStaked'])
    df['stakePercentage'] = None

    # activity = stakes + votes + proposals
    df['activity'] = 0

    # calculate new metrics
    for i, row in df.iterrows():
        df.loc[i, 'activity'] = row['nStakes'] + row['nVotes'] + row['nProposals'] 
        if row['nProposals'] > 0:
            df.loc[i, 'boostPercentage'] = row['nBoost'] / row['nProposals'] * 100
            df.loc[i, 'stakePercentage'] = row['nPropStaked'] / row['nProposals'] * 100
            df.loc[i, 'acceptedPercentage'] = row['nPropAccepted'] / row['nProposals'] * 100
            df.loc[i, 'rejectedPercentage'] = row['nPropRejected'] / row['nProposals'] * 100

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
    df = df[df['daoName'] != 'Kyber DAO Exp#2']
    # df = df[df['daoName'] != 'Genesis Alpha']
    # df = df[df['daoName'] != 'dxDAO']
    # df = df[df['daoName'] != 'necDAO']
    # df = df[df['activityPercentage'] > 50]
    # print(df[['nUsers', 'nProposals', 'nBoost', 'nPropAccepted', 'nPropRejected']].corr(method='pearson'))
    # print(df[['nUsers', 'nProposals', 'nPropAccepted', 'nPropRejected', 'nPropStaked', 'nBoost']].corr(method='spearman'))
    
    df = df.rename(columns={'nUsers': 'Users', 'stakePercentage': 'Staked proposals %'})

    sns.set(style="white", color_codes=True)
    j = sns.jointplot(
        x=df["Users"], 
        y=df["Staked proposals %"], 
        kind='scatter', 
        s=100, 
        color=PLOT_COLOR, 
        edgecolor='black', 
        linewidth=0.7,
        alpha=0.5)

    # j.annotate(stats.pearsonr)
    # j.annotate(stats.spearmanr)

    plt.show()

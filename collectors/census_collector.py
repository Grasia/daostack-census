import os
import pandas as pd
from typing import Dict, List, Set
from datetime import datetime
from requester import n_requests

daos_ids: Set[str] = set()


# queries
DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name reputationHoldersCount}}}}'

EVENT_QUERY: str = '{{events(where: {{type: "NewDAO"}}, first: {0}, skip: {1}\
){{timestamp dao{{id}}}}}}'

PROPOSAL_QUERY: str = '{{proposals(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{id}}}}'

VOTES_QUERY: str = '{{proposalVotes(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{id}}}}'

STAKES_QUERY: str = '{{proposalStakes(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{id}}}}'


def get_daos() -> pd.DataFrame:
    """
    Gets all DAOs id, name and number of users.
    """
    print("Requesting DAOs ...")
    start: datetime = datetime.now()

    daos: List[Dict] = n_requests(query=DAO_QUERY, result_key='daos')

    print(f'DAOs requested in {(datetime.now() - start).total_seconds():.2}s')

    dff: pd.DataFrame = pd.DataFrame(daos)
    dff = dff.rename(columns={"reputationHoldersCount": "nUsers"})

    global daos_ids
    daos_ids = set(dff['id'].tolist())

    return dff


def get_daos_birth() -> pd.DataFrame:
    print("Requesting DAOs birth ...")
    start: datetime = datetime.now()

    events: List[Dict] = n_requests(query=EVENT_QUERY, result_key='events')

    print(f'DAOs birth requested in {round((datetime.now() - start).total_seconds(), 2)}s')

    daos: List[Dict] = list()
    for e in events:
        if e['dao']['id'] in daos_ids:
            daos.append({
                'id': e['dao']['id'],
                'birth': e['timestamp']
            })

    return pd.DataFrame(daos)


def get_proposals() -> pd.DataFrame:
    """
    Gets a dataframe with DAOs id and them number of proposals
    """
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'nProposals'])
    print("Requesting proposals ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, 
            result_key='proposals', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(proposals)
        dff = dff.rename(columns={"id": "pId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='nProposals')
        if len(proposals) == 0:
            dff = {'id': d_id, 'nProposals': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Proposals requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


def get_votes() -> pd.DataFrame:
    """
    Gets a dataframe with DAOs ids and them number of votes
    """
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'nVotes'])
    print("Requesting votes ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        votes: List[Dict] = n_requests(query=VOTES_QUERY, 
            result_key='proposalVotes', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(votes)
        dff = dff.rename(columns={"id": "vId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='nVotes')
        if len(votes) == 0:
            dff = {'id': d_id, 'nVotes': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Votes requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


def get_stakes() -> pd.DataFrame:
    """
    Gets a dataframe with DAOs ids and them number of stakes
    """
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'nStakes'])
    print("Requesting stakes ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        stakes: List[Dict] = n_requests(query=STAKES_QUERY, 
            result_key='proposalStakes', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(stakes)
        dff = dff.rename(columns={"id": "sId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='nStakes')
        if len(stakes) == 0:
            dff = {'id': d_id, 'nStakes': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Stakes requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


def join_df_by_id(df1: pd.DataFrame, df2: pd.DataFrame, keys: List[str])\
-> pd.DataFrame:

    df: pd.DataFrame = df1
    # initialization
    for k in keys:
        df[k] = None

    for i, row in df.iterrows():
        try:
            r = df2[df2['id'] == row['id']]
            for k in keys:
                df.loc[i, k] = r.iloc[0][k]
        except:
            print(f'Error with {row["name"]}')

    return df


if __name__ == '__main__':
    # load holdings
    filename: str = ''
    for (dirpath, dirnames, filenames) in os.walk('datawarehouse'):
        for file in filenames:
            if 'dao_holdings' in file:
                filename = os.path.join(dirpath, file)  

    df: pd.DataFrame = get_daos()
    df2: pd.DataFrame = get_daos_birth()
    df3: pd.DataFrame = get_proposals()
    df4: pd.DataFrame = get_votes()
    df5: pd.DataFrame = get_stakes()
    df6: pd.DataFrame = pd.read_csv(filename, header=0)

    df = join_df_by_id(df1=df, df2=df2, keys=['birth'])
    df = join_df_by_id(df1=df, df2=df3, keys=['nProposals'])
    df = join_df_by_id(df1=df, df2=df4, keys=['nVotes'])
    df = join_df_by_id(df1=df, df2=df5, keys=['nStakes'])
    df = join_df_by_id(df1=df, df2=df6, keys=['ETH', 'GEN', 'otherTokens'])

    out_file: str = os.path.join('datawarehouse', 'census.csv')
    df.to_csv(out_file, index=False)
    print(f'DONE. Data stored in {out_file}')

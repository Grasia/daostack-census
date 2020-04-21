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
    dff = dff.rename(columns={"reputationHoldersCount": "n_users"})

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
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'n_proposals'])
    print("Requesting proposals ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, 
            result_key='proposals', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(proposals)
        dff = dff.rename(columns={"id": "pId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='n_proposals')
        if len(proposals) == 0:
            dff = {'id': d_id, 'n_proposals': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Proposals requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


def get_votes() -> pd.DataFrame:
    """
    Gets a dataframe with DAOs ids and them number of votes
    """
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'n_votes'])
    print("Requesting votes ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        votes: List[Dict] = n_requests(query=VOTES_QUERY, 
            result_key='proposalVotes', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(votes)
        dff = dff.rename(columns={"id": "vId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='n_votes')
        if len(votes) == 0:
            dff = {'id': d_id, 'n_votes': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Votes requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


def get_stakes() -> pd.DataFrame:
    """
    Gets a dataframe with DAOs ids and them number of stakes
    """
    df: pd.DataFrame = pd.DataFrame(columns=['id', 'n_stakes'])
    print("Requesting stakes ...")
    start: datetime = datetime.now()

    for d_id in daos_ids:
        stakes: List[Dict] = n_requests(query=STAKES_QUERY, 
            result_key='proposalStakes', dao_id=d_id)

        dff: pd.DataFrame = pd.DataFrame(stakes)
        dff = dff.rename(columns={"id": "sId"})
        dff['id'] = d_id
        dff = dff.groupby('id').size().reset_index(name='n_stakes')
        if len(stakes) == 0:
            dff = {'id': d_id, 'n_stakes': 0}

        df = df.append(dff, ignore_index=True)

    print(f'Stakes requested in {(datetime.now() - start).total_seconds():.2}s')
    return df


if __name__ == '__main__':
    df: pd.DataFrame = get_daos()
    df2: pd.DataFrame = get_daos_birth()
    df3: pd.DataFrame = get_proposals()
    df4: pd.DataFrame = get_votes()
    df5: pd.DataFrame = get_stakes()

    df['birth'] = 0
    df['n_proposals'] = df3['n_proposals'].tolist()
    df['n_votes'] = df4['n_votes'].tolist()
    df['n_stakes'] = df5['n_stakes'].tolist()
    df['ETH'] = 0.0
    df['GEN'] = 0.0
    df['otherTokens'] = 0.0

    # add DAOs birth
    for i, row in df.iterrows():
        r = df2[df2['id'] == row['id']]
        df.loc[i, 'birth'] = r.iloc[0]['birth']

    # load holdings
    filename: str = ''
    for (dirpath, dirnames, filenames) in os.walk('datawarehouse'):
        for file in filenames:
            if 'dao_holdings' in file:
                filename = os.path.join(dirpath, file)  

    df6: pd.DataFrame = pd.read_csv(filename, header=0)

    # add holdings by id
    for i, row in df.iterrows():
        r = df6[df6['id'] == row['id']]
        df.loc[i, 'ETH'] = r.iloc[0]['ETH']
        df.loc[i, 'GEN'] = r.iloc[0]['GEN']
        df.loc[i, 'otherTokens'] = r.iloc[0]['otherTokens']


    out_file: str = os.path.join('datawarehouse', 'census.csv')
    df.to_csv(out_file, index=False)
    print(f'DONE. Data stored in {out_file}')

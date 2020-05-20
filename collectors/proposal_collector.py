import os
import pandas as pd
from typing import Dict, List
from datetime import datetime
from requester import n_requests

DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name}}}}'

PROPOSAL_QUERY: str = '{{proposals(where: {{dao: "{0}", executedAt_not: null}}, first: {1}, skip: {2}\
){{id createdAt boostedAt totalRepWhenExecuted votesFor votesAgainst stakesFor stakesAgainst winningOutcome \
stakes{{staker}}}}}}'


def get_daos_id() -> pd.DataFrame:
    print("Requesting DAO ids ...")
    start: datetime = datetime.now()

    daos: List[Dict] = n_requests(query=DAO_QUERY, result_key='daos')

    print(f'DAO ids requested in {round((datetime.now() - start).total_seconds(), 2)}s')

    return pd.DataFrame(daos)


def get_proposals(daos: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()

    print("Requesting proposals ...")
    start: datetime = datetime.now()

    for _, row in daos.iterrows():
        proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, 
            result_key='proposals', dao_id=row['id'])

        # calculate diferent stakers
        for p in proposals:
            p['differentStakers'] = len(set([x['staker'] for x in p['stakes']]))
            del p['stakes']

        dff: pd.DataFrame = pd.DataFrame(proposals)
        dff = dff.rename(columns={'id': 'proposalId', 'winningOutcome': 'hasPassed'})
        dff['daoId'] = row['id']
        dff['daoName'] = row['name']
        df = df.append(dff, ignore_index=True)

    print(f'Proposals requested in {round((datetime.now() - start).total_seconds(), 2)}s')

    # data transformation 
    df['hasPassed'] = df['hasPassed'].apply(lambda x: True if x == 'Pass' else False)
    df['createdAt'] = df['createdAt'].apply(lambda x: int(x))
    df['differentStakers'] = df['differentStakers'].apply(lambda x: int(x))

    return df


if __name__ == '__main__':
    daos: pd.DataFrame = get_daos_id()
    df: pd.DataFrame = get_proposals(daos)
    df = df[df['createdAt'] <= 1587596397]

    # column reorder
    df = df[[
        'daoId', 
        'daoName', 
        'proposalId', 
        'createdAt', 
        'totalRepWhenExecuted', 
        'votesFor',
        'votesAgainst',
        'hasPassed',
        'boostedAt',
        'stakesFor',
        'stakesAgainst',
        'differentStakers']]

    out_file: str = os.path.join('datawarehouse', 'proposals.csv')
    df.to_csv(out_file, index=False)
    print(f'DONE. Data stored in {out_file}')
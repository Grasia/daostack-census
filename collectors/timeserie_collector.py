import os
import pandas as pd
from typing import Dict, List
from datetime import datetime
from requester import n_requests
import time

DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name}}}}'

PROPOSAL_QUERY: str = '{{proposals(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{proposer createdAt}}}}'

VOTE_QUERY: str = '{{proposalVotes(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{voter createdAt}}}}'

STAKE_QUERY: str = '{{proposalStakes(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{staker createdAt}}}}'


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
        try:
            proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, 
                result_key='proposals', dao_id=row['id'])
        except Exception as e:
            print(e)
            time.sleep(45)
            proposals: List[Dict] = n_requests(query=PROPOSAL_QUERY, 
                result_key='proposals', dao_id=row['id'])
            print('Recovered: resuming requests')

        finally:
            dff: pd.DataFrame = pd.DataFrame(proposals)
            dff = dff.rename(columns={'proposer': 'userId', 'createdAt': 'unixDate'})
            dff['daoId'] = row['id']
            dff['daoName'] = row['name']
            dff['actionType'] = 'proposal'
            df = df.append(dff, ignore_index=True)

    print(f'Proposals requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return df


def get_votes(daos: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()

    print("Requesting votes ...")
    start: datetime = datetime.now()

    for _, row in daos.iterrows():
        try:
            votes: List[Dict] = n_requests(query=VOTE_QUERY, 
                result_key='proposalVotes', dao_id=row['id'])
        except Exception as e:
            print(e)
            time.sleep(45)
            votes: List[Dict] = n_requests(query=VOTE_QUERY, 
                result_key='proposalVotes', dao_id=row['id'])
            print('Recovered: resuming requests')

        finally:
            dff: pd.DataFrame = pd.DataFrame(votes)
            dff = dff.rename(columns={'voter': 'userId', 'createdAt': 'unixDate'})
            dff['daoId'] = row['id']
            dff['daoName'] = row['name']
            dff['actionType'] = 'vote'
            df = df.append(dff, ignore_index=True)

    print(f'Votes requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return df


def get_stakes(daos: pd.DataFrame) -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()

    print("Requesting stakes ...")
    start: datetime = datetime.now()

    for _, row in daos.iterrows():
        try:
            stakes: List[Dict] = n_requests(query=STAKE_QUERY, 
                result_key='proposalStakes', dao_id=row['id'])
        except Exception as e:
            print(e)
            time.sleep(45)
            stakes: List[Dict] = n_requests(query=STAKE_QUERY, 
                result_key='proposalStakes', dao_id=row['id'])
            print('Recovered: resuming requests')

        finally:
            dff: pd.DataFrame = pd.DataFrame(stakes)
            dff = dff.rename(columns={'staker': 'userId', 'createdAt': 'unixDate'})
            dff['daoId'] = row['id']
            dff['daoName'] = row['name']
            dff['actionType'] = 'stake'
            df = df.append(dff, ignore_index=True)

    print(f'Stakes requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    return df


if __name__ == '__main__':
    daos: pd.DataFrame = get_daos_id()
    time.sleep(30)
    df: pd.DataFrame = get_proposals(daos)
    time.sleep(30)
    df = df.append(get_votes(daos), ignore_index=True)
    time.sleep(30)
    df = df.append(get_stakes(daos), ignore_index=True)

    # column reorder
    df = df[['daoId', 'daoName', 'actionType', 'unixDate', 'userId']]

    out_file: str = os.path.join('datawarehouse', 'activity_serie.csv')
    df.to_csv(out_file, index=False)
    print(f'DONE. Data stored in {out_file}')

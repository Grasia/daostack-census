import json
import pandas as pd
from graphqlclient import GraphQLClient
from typing import Dict, List
from datetime import datetime


ELEMS_PER_CHUNK: int = 1000
DAOSTACK_URL: str = 'https://api.thegraph.com/subgraphs/name/daostack/master'
client: GraphQLClient = GraphQLClient(DAOSTACK_URL)
daos_ids: List[str] = list()

# queries
DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name reputationHoldersCount}}}}'

PROPOSAL_QUERY: str = '{{proposals(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{id}}}}'


def request(query: str) -> Dict:
    """
    Requests data from endpoint.
    """
    result = client.execute(query)
    result = json.loads(result)
    return result['data'] if 'data' in result else dict()


def n_requests(query: str, result_key: str, dao_id: str = '') -> List[Dict]:
    """
    Requests all chunks from endpoint.

    Parameters:
        * query: json to request
        * result_key 
        * dao_id
    """
    elements: List[Dict] = list()
    chunk: int = 0
    result = Dict
    condition: bool = True

    while condition:
        if dao_id:
            query_filled: str = query.format(dao_id, ELEMS_PER_CHUNK, len(elements))
        else:
            query_filled: str = query.format(ELEMS_PER_CHUNK, len(elements))

        result = request(query=query_filled)
        result = result[result_key]

        elements.extend(result)

        condition = len(result) == ELEMS_PER_CHUNK
        chunk += 1

    return elements


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
    daos_ids = dff['id'].tolist()

    return dff


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


if __name__ == '__main__':
    df1: pd.DataFrame = get_daos()
    df2: pd.DataFrame = get_proposals()

    df = df1
    df['n_proposals'] = df2['n_proposals'].tolist()
    print(df)

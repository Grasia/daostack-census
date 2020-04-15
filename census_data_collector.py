import json
import pandas as pd
from graphqlclient import GraphQLClient
from typing import Dict, List, Callable
from datetime import datetime


ELEMS_PER_CHUNK: int = 1000
DAOSTACK_URL: str = 'https://api.thegraph.com/subgraphs/name/daostack/master'
client: GraphQLClient = GraphQLClient(DAOSTACK_URL)
df: pd.DataFrame = pd.DataFrame(columns=['id', 'name', 'users'])

# queries
DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id name reputationHoldersCount}}}}'


def request(query: str) -> Dict:
    """
    Requests data from endpoint.
    """
    result = client.execute(query)
    result = json.loads(result)
    return result['data'] if 'data' in result else dict()


def n_requests(query: str, result_key: str) -> List[Dict]:
    """
    Requests all chunks from endpoint.

    Parameters:
        * query: json to request
        * result_key 
    """
    elements: List[Dict] = list()
    chunk: int = 0
    result = Dict
    condition: bool = True

    while condition:
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
    dff = dff.rename(columns={"reputationHoldersCount": "users"})
    return dff


if __name__ == '__main__':
    df = get_daos()

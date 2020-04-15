import json
from graphqlclient import GraphQLClient
from typing import Dict


ELEMS_PER_CHUNK = 1000
DAOSTACK_URL = 'https://api.thegraph.com/subgraphs/name/daostack/master'
client = GraphQLClient(DAOSTACK_URL)


def request(query: str) -> Dict:
    """
    Requests data from endpoint.
    """
    result = client.execute(query)
    result = json.loads(result)
    return result['data'] if 'data' in result else dict()


if __name__ == '__main__':
    #print(request('{daos(first: 1){name}}'))

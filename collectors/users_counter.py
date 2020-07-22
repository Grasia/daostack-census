from datetime import datetime
from typing import Dict, List, Set
from requester import n_requests

DAO_QUERY: str = '{{daos(where: {{register: "registered"}}, first: {0}, skip: {1}\
){{id}}}}'

USER_QUERY: str = '{{reputationHolders(where: {{dao: "{0}"}}, first: {1}, skip: {2}\
){{address}}}}'

if __name__ == '__main__':
    print("Requesting DAOs ...")
    start: datetime = datetime.now()
    daos: List[Dict] = n_requests(query=DAO_QUERY, result_key='daos')
    print(f'DAOs requested in {round((datetime.now() - start).total_seconds(), 2)}s')
    daos = [d['id'] for d in daos]

    print("Requesting users ...")
    start: datetime = datetime.now()
    users = list()
    for d in daos:
        aux: List[Dict] = n_requests(query=USER_QUERY, 
            result_key='reputationHolders', dao_id=d)
        users = users + aux

    print(f'Users requested in {round((datetime.now() - start).total_seconds(), 2)}s')


    users: List[str] = [u['address'] for u in users]
    print(f'Total users = {len(users)}')
    users: Set[str] = set(users)
    print(f'Total different users = {len(users)}')

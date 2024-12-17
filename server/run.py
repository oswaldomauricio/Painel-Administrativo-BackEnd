from infra.controllers.users_controller import UsersResponse
from infra.configs.connection import DBconnection
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

repo = UsersResponse()

data = repo.select()

for indice in range(len(data)):
    dataDict = dict({
        'id': data[indice].ID,
        'userName': data[indice].NAME,
        'password': data[indice].PASSWORD

    })
    print(dataDict)

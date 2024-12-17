from infra.controllers.users_controller import UsersResponse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

repo = UsersResponse()

# data = repo.select()
data = repo.insert('teste123', '12345', 76)
print(data)

# for indice in range(len(data)):
#     dataDict = dict({
#         'id': data[indice].ID,
#         'userName': data[indice].NAME,
#         'password': data[indice].PASSWORD

#     })
#     print(dataDict)

from flask import Blueprint, request, jsonify
from infra.controllers.users_controller import UsersResponse
from infra.controllers.stores_users_controller import ResponseStoreUser
from infra.controllers.stores_users_controller import StoreUsersController

# Inicialize o Blueprint
store_users_bp = Blueprint('stores_users', __name__)

# Inicialize as dependências
response_users = UsersResponse()
response_store_users = ResponseStoreUser()

# Instancie o controlador
store_users_controller = StoreUsersController(response_users, response_store_users)

# Rota para obter usuário e lojas
@store_users_bp.route('/usuario/lojas', methods=['POST'])
def get_store_by_user():
    try:
        req_user = request.get_json()
        name = req_user.get('name')
        password = req_user.get('password')

        # Chama a função reutilizável
        result = store_users_controller.get_store_by_user(name, password)

        # Retorna a resposta apropriada
        if result.get('status') == 200:
            return jsonify({'user': result['user'], 'stores': result['stores']}), 200
        return jsonify({'error': result['error']}), result.get('status', 500)
    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro interno: {e}'}), 500



#caso eu queira chamar essa função em outro arquivo, devo usar o seguinte codigo.

# from store_users_controller import StoreUsersController
# from infra.controllers.users_controller import UsersResponse
# from infra.controllers.stores_users_controller import ResponseStoreUser

# # Inicialize as dependências
# response_users = UsersResponse()
# response_store_users = ResponseStoreUser()

# # Instancie o controlador
# store_users_controller = StoreUsersController(response_users, response_store_users)

# # Use a função em outro contexto
# def check_user_and_stores():
#     name = "test_user"
#     password = "1234"

#     result = store_users_controller.get_store_by_user(name, password)

#     if result.get('status') == 200:
#         print(f"User: {result['user']}")
#         print(f"Stores: {result['stores']}")
#     else:
#         print(f"Error: {result['error']}")

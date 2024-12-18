from flask import Blueprint, request, jsonify
from infra.controllers.users_controller import UsersResponse
from infra.controllers.stores_users_controller import ResponseStoreUser
from flask_pydantic_spec import FlaskPydanticSpec # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.

store_users_bp = Blueprint('stores_users', __name__)

response_users = UsersResponse()
response_store_users = ResponseStoreUser()

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(store_users_bp)

# Rota GET por Nome e Senha
@store_users_bp.route('/usuario/lojas', methods=['GET'])
def get_store_by_user():
    try:
        req_user = request.get_json()

        name = req_user.get('name')
        password = req_user.get('password')

        if not name or not password:
            return jsonify({'error': 'Nome e senha são obrigatórios!'}), 400

        users = response_users.select()
        stores_users = response_store_users.select()

        users_to_dict = [user.to_dict() for user in users]
        stores_to_dict = [store.to_dict() for store in stores_users]

        for user in users_to_dict:
            if user['name'] == name and user['password'] == password:
                user_stores = [
                    store for store in stores_to_dict if store['id_users'] == user['id']
                ]
                return jsonify({'user': user, 'stores': user_stores}), 200

        # Caso nenhum usuário seja encontrado
        return jsonify({'error': 'Informações inválidas ou usuário não encontrado!'}), 404

    except Exception as e:
        return jsonify({'error': f'Ocorreu um erro interno: {e}'}), 500
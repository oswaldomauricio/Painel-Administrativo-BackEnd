from flask import Blueprint, request, jsonify
from infra.controllers.users_controller import UsersResponse

# Criando o Blueprint para usuários
users_bp = Blueprint('users', __name__)

response_users = UsersResponse()

# Rota GET para todos os usuários
@users_bp.route('/usuario', methods=['GET'])
def get_users():
    data = response_users.select()
    data_to_dict = [user.to_dict() for user in data]
    return jsonify(data_to_dict)



# Rota GET por ID
@users_bp.route('/usuario/<int:id>', methods=['GET'])
def get_users_by_id(id):
    data = response_users.select()
    data_to_dict = [user.to_dict() for user in data]

    for i, users in enumerate(data_to_dict):
        if users['id'] == id:
            return jsonify(users)



# Rota POST para inserir usuário
@users_bp.route('/usuario', methods=['POST'])
def insert_user():
    try:
        new_user = request.get_json()
        id = new_user.get('id')
        nome = new_user.get('nome')
        password = new_user.get('password')

        if id and nome and password:
            response_users.insert(nome, password, id)
            return jsonify({
                'ok': f'registro inserido com sucesso [{id}], [{nome}], [{password}]'
            }), 201
        return jsonify({"error": "Faltou alguma informação para criação do usuário"}), 400

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500
    


# Rota DELETE por ID
@users_bp.route('/usuario/<int:id>', methods=['DELETE'])
def delete_user_by_id(id):
    response_users.delete(id)
    return jsonify({'ok': f'Registro deletado com sucesso (ID: {id})'})



# Rota PUT para atualizar usuário
@users_bp.route('/usuario/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        updated_user = request.get_json()
        nome = updated_user.get('nome')
        password = updated_user.get('password')

        if nome and password:
            response_users.update(nome, password, id)
            return jsonify({
                'ok': f'Registro alterado com sucesso. {id}, {nome}, {password}'
            }), 200
        return jsonify({"error": "Faltou alguma informação para atualizar o usuário"}), 400

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500

from flask import Blueprint, request, jsonify
from infra.controllers.users_controller import UsersResponse
from flask_pydantic_spec import FlaskPydanticSpec # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.

users_bp = Blueprint('users', __name__)

response_users = UsersResponse()

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(users_bp)

# Rota GET por Nome e Senha
@users_bp.route('/usuario', methods=['GET'])
def get_users_by_name_and_pass():
    req_user = request.get_json()

    name = req_user.get('name')
    password = req_user.get('password')

    if not name or not password:
        return jsonify({'error': 'Nome e senha são obrigatórios!'}), 400

    get_user = {
        "name": name,
        "password": password
    }

    data = response_users.select()

    data_to_dict = [user.to_dict() for user in data]

    if get_user['name'] and get_user['password']:
        for i, users in enumerate(data_to_dict):
            if users['name'] == get_user['name'] and users['password'] == get_user['password']:
                return jsonify({'result': users, 'status': 200})
        else:
            return jsonify({'error': 'informação invalidas ou vazias, favor, verifique seu cadastro!'}), 400
    

# Rota POST para inserir usuário
@users_bp.route('/usuario', methods=['POST'])
def insert_user():
    try:
        new_user = request.get_json()
        # id = new_user.get('id')
        nome = new_user.get('name')
        password = new_user.get('password')

        if not nome or not password:
            return jsonify({'error': 'Nome e senha são obrigatórios!'}), 400

        if id and nome and password:
            response_users.insert(nome, password)
            users = {
                'name': nome,
                'password': password
            }
            return jsonify({
                "usuario": users,
                "result": "Registro incluido com sucesso.",
                "status": 200
            })
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
        nome = updated_user.get('name')
        password = updated_user.get('password')

        if nome and password:
            response_users.update(nome, password, id)
            return jsonify({
                'ok': f'Registro alterado com sucesso. {id}, {nome}, {password}'
            }), 200
        return jsonify({"error": "Faltou alguma informação para atualizar o usuário"}), 400

    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro interno: {e}"}), 500

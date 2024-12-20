from flask import Blueprint, request, jsonify
from infra.controllers.cash_box_controller import ResponseCashBox
from flask_pydantic_spec import FlaskPydanticSpec # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.

cashbox_bp = Blueprint('cash box', __name__)

response_cashbox = ResponseCashBox()

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(cashbox_bp)

# Rota GET por Nome e Senha
@cashbox_bp.route('/cashbox', methods=['GET'])
def get_cashbox_by_store_and_tipo_operacao():
    req_cashbox = request.get_json()

    id_loja = req_cashbox.get('id_loja')
    tipo_operacao = req_cashbox.get('tipo_operacao')

    if not id_loja or not tipo_operacao:
        return jsonify({'error': 'loja e o tipo de operação não informado!'}), 400

    get_info = {
        "id_loja": id_loja,
        "tipo_operacao": tipo_operacao
    }

    data = response_cashbox.select()

    data_to_dict = [infos.to_dict() for infos in data]

    return jsonify(data_to_dict)

    # if get_info['name'] and get_user['password']:
    #     for i, users in enumerate(data_to_dict):
    #         if users['name'] == get_user['name'] and users['password'] == get_user['password']:
    #             return jsonify(users), 200
    #     else:
    #         return jsonify({'error': 'informação invalidas ou vazias, favor, verifique seu cadastro!'}), 400
    

from flask import Blueprint, request, jsonify
from infra.controllers.cash_box_controller import ResponseCashBox
from infra.controllers.cash_box_controller import CashBoxController
from infra.controllers.cash_box_controller import ResponseCashBox
from flask_pydantic_spec import FlaskPydanticSpec # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.
cashbox_bp = Blueprint('cash box', __name__)

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(cashbox_bp)

response_cashBox = ResponseCashBox()

# Instancie o controlador
CashBox_Controller = CashBoxController(response_cashBox)

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

    result = CashBox_Controller.select_all_info_by_cashBox(get_info['id_loja'], get_info['tipo_operacao'])
    print(result.get_json())  # Para extrair os dados JSON
    return result.get_json()
    

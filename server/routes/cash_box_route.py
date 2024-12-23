from flask import Blueprint, request, jsonify
from infra.controllers.cash_box_controller import ResponseCashBox
from infra.controllers.cash_box_controller import CashBoxController
from infra.controllers.cash_box_controller import ResponseCashBox
from flask_pydantic_spec import FlaskPydanticSpec # type: ignore # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.
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
    date_operacao = req_cashbox.get('data')

    if not id_loja and not date_operacao:
        return jsonify({'error': 'loja e a data não foram informados, favor verificar!'}), 400

    get_info = {
        "id_loja": id_loja,
        "date": date_operacao
    }

    result = CashBox_Controller.select_all_info_by_cashBox(get_info['id_loja'], get_info['date'])
    print(result.get_json())
    return result.get_json()
    

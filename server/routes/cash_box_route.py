from flask import Blueprint, request, jsonify
from infra.controllers.cash_box_controller import ResponseCashBox
from infra.controllers.cash_box_controller import CashBox_select_Controller
from infra.controllers.cash_box_controller import CashBox_insert_Controller
from infra.controllers.cash_box_controller import cashBox_delete_controller
from infra.controllers.cash_box_controller import ResponseCashBox
from flask_pydantic_spec import FlaskPydanticSpec # type: ignore # Cria um endpoint chamado /doc/swagger que mostra os endpoints que tenho na minha aplicação.
cashbox_bp = Blueprint('cash box', __name__)

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(cashbox_bp)

response_cashBox = ResponseCashBox()

# Instancie o controlador
CashBox_select = CashBox_select_Controller(response_cashBox)
CashBox_insert = CashBox_insert_Controller(response_cashBox)
CashBox_delete = cashBox_delete_controller(response_cashBox)

# Rota GET por Nome e Senha
@cashbox_bp.route('/cashbox/relatorio', methods=['POST'])
def get_cashbox_by_store_and_tipo_operacao():
    req_cashbox = request.get_json()

    loja = req_cashbox.get('loja')
    date_operacao = req_cashbox.get('data')

    if not loja and not date_operacao:
        return jsonify({'error': 'loja e a data não foram informados, favor verificar!'}), 400

    get_info = {
        "loja": loja,
        "date": date_operacao
    }
    print(get_info)

    result = CashBox_select.select_all_info_by_cashBox(get_info['loja'], get_info['date'])
    return result.get_json()


@cashbox_bp.route('/cashbox', methods=['POST'])
def insert_cashbox():
    req_cashbox = request.get_json()

    loja = req_cashbox.get('loja')
    id_user = req_cashbox.get('id_user')
    date_operacao = req_cashbox.get('data')
    tipo_operacao = req_cashbox.get('tipo_operacao')
    valor = req_cashbox.get('valor')
    numero_doc = req_cashbox.get('numero_doc')
    origem = req_cashbox.get('origem')


    if not loja or not id_user or not date_operacao or not valor or not tipo_operacao:
        return jsonify({'error': 'ah informações faltando, favor, verificar!'}), 400

    get_info = {
        "loja": loja,
        "date": date_operacao,
        "tipo_operacao": tipo_operacao,
        "valor": valor,
        "numero_doc": numero_doc,
        "origem": origem,
        "id_user": id_user,
        "status": 1
    }
    print(get_info)

    select_id = CashBox_select.response_CashBox.select()
    ids = [item.ID for item in select_id]
    max_id = max(ids) #aqui eu to pegando o id maximo da tabela para poder fazer o insert pois o oracle tava dando ele como null
    max_id +=1

    result = CashBox_insert.insert_info_cashbox(max_id+1, get_info['loja'], get_info['date'], get_info['tipo_operacao'], get_info['valor'], get_info['status'], get_info['numero_doc'], get_info['origem'], get_info['id_user'])
    
    
    return result.get_json()

@cashbox_bp.route('/cashbox', methods=['PUT'])
def delete_cashbox():
    """
    esse metodo não exclui o registro do banco, apenas altera o valor do status para 0 e a funcao para calcular o saldo ignora os que tem 0 no status.
    isso serve para que tenha registro dos itens que foram excluidos!
    """
    req_cashbox = request.get_json()

    id = req_cashbox.get('id')
    if not id:
        return jsonify({'error': 'não foi localizado o caixa inserido, favor verifique!'}), 400

    get_info = {
        "id": id,
        "status": 0
    }

    result = CashBox_delete.delete_info_cashbox(get_info['id'], get_info['status'])
    return result.get_json()

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from infra.controllers.cash_box_controller import ResponseCashBox
from infra.controllers.cash_box_controller import CashBox_select_Controller
from infra.controllers.cash_box_controller import CashBox_insert_Controller
from infra.controllers.cash_box_controller import cashBox_delete_controller
from infra.controllers.cash_box_controller import ResponseCashBox
from flask_pydantic_spec import FlaskPydanticSpec
cashbox_bp = Blueprint('cash box', __name__)

spec = FlaskPydanticSpec('Flask', titulo='API - NORTE AUTO PEÇAS')
spec.register(cashbox_bp)

response_cashBox = ResponseCashBox()

CashBox_select = CashBox_select_Controller(response_cashBox)
CashBox_insert = CashBox_insert_Controller(response_cashBox)
CashBox_delete = cashBox_delete_controller(response_cashBox)
CashBox_edit = cashBox_edit_controller(response_cashBox)

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

    result = CashBox_select.select_all_info_by_cashBox(get_info['loja'], get_info['date'])
    logging.info("relatorio de caixa (data e loja): %s", result.get_json())
    return result.get_json()

# Relatorio de caixa por periodo selecionado.
@cashbox_bp.route('/cashbox/relatorio/periodo', methods=['POST'])
def get_cashbox_per_period_and_store():
    req_cashbox = request.get_json()

    loja = req_cashbox.get('loja')
    data_inicial = req_cashbox.get('data_inicial')
    data_final = req_cashbox.get('data_final')

    if not loja:
        return jsonify({'error': 'loja e a data não foram informados, favor verificar!'}), 400
    
    if not data_inicial and not data_final:
        return jsonify({'error': 'loja e a data não foram informados, favor verificar!'}), 400

    get_info = {
        "loja": loja,
        "data_inicial": data_inicial,
        "data_final": data_final
    }

    result = CashBox_select.select_all_info_per_period(get_info['loja'], get_info['data_inicial'], get_info['data_final'])
    logging.info("relatorio de caixa periodo (data inicial, data final e loja): %s", result.get_json())
    return result.get_json()

# Inserir valor no relatorio de caixa.
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
    tipo = req_cashbox.get('tipo')


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
        "status": 1,
        "tipo": tipo
    }

    select_id = CashBox_select.response_CashBox.select()
    ids = [item.ID for item in select_id]
    max_id = max(ids) #aqui eu to pegando o id maximo da tabela para poder fazer o insert pois o oracle tava dando ele como null
    max_id +=1

    result = CashBox_insert.insert_info_cashbox(max_id+1, get_info['loja'], get_info['date'], get_info['tipo_operacao'], get_info['valor'], get_info['status'], get_info['numero_doc'], get_info['origem'], get_info['id_user'], get_info['tipo'])
    
    logging.info("Inserção de valor: %s", result.get_json())
    return result.get_json()

# alterar status do valor para ser excluido.
@cashbox_bp.route('/cashbox', methods=['PUT'])
def delete_cashbox():
    """
    Esse método não exclui o registro do banco, apenas altera o valor do status para 0.
    A função que calcula o saldo ignora registros com status 0.
    Isso permite manter um histórico dos itens excluídos.
    """

    req_cashbox = request.get_json()

    id = req_cashbox.get('id')
    user_role = req_cashbox.get('role')  # Cargo do usuário (exemplo: "ADMIN" ou "USER")

    if not id or not user_role:
        return jsonify({'error': 'Informações incompletas, favor verificar!'}), 400

    # Buscar informações do caixa para validar a data da inserção e o usuário original
    cashbox_record = ResponseCashBox.get_caixa_by_id(id)

    print(cashbox_record)

    if not cashbox_record:
        return jsonify({'error': 'Registro não encontrado!'}), 404

    data_insercao = cashbox_record.DATA 
    data_atual = datetime.today().date()

    # Regra: ADMIN pode alterar status a qualquer momento
    if user_role == "ADMIN":
        status = 0
    else:
        # Se não for ADMIN, só pode alterar se for o mesmo usuário e no mesmo dia
        if data_insercao != data_atual:
            return jsonify({'error': 'Só é possível excluir registros no mesmo dia da inserção!'}), 403

        status = 0  # Permite alteração do status

    result = CashBox_delete.delete_info_cashbox(id, status)
<<<<<<< Updated upstream
    logging.info("Remoção de valor do caixa: %s", result.get_json())
=======
    logging.info("Remoção de valor do caixa: %s", id, result.get_json())
    return result.get_json()


@cashbox_bp.route('/cashbox/edit', methods=['PUT'])
def edit_cashbox():
    """
    Esse método não exclui o registro do banco, apenas altera o valor do status para 0.
    A função que calcula o saldo ignora registros com status 0.
    Isso permite manter um histórico dos itens excluídos.
    """

    req_cashbox = request.get_json()

    id = req_cashbox.get('id')
    num_doc = req_cashbox.get('num_doc')
    origem = req_cashbox.get('origem')
    valor = req_cashbox.get('valor')
    tipo = req_cashbox.get('tipo')
    user_role = req_cashbox.get('role')  # Cargo do usuário (exemplo: "ADMIN" ou "USER")

    if not id or not user_role or not num_doc or not origem or not valor or not tipo:
        return jsonify({'error': 'Informações incompletas, favor verificar!'}), 400

    cashbox_record = ResponseCashBox.get_caixa_by_id(id)

    if not cashbox_record:
        return jsonify({'error': 'Registro não encontrado!'}), 404

    data_insercao = cashbox_record.DATA 
    data_atual = datetime.today().date()

    if user_role == "ADMIN":
        status = 0
    else:
        if data_insercao != data_atual:
            return jsonify({'error': 'Só é possível excluir registros no mesmo dia da inserção!'}), 403

        status = 0  

    result = CashBox_delete.delete_info_cashbox(id, status)
    logging.info("Remoção de valor do caixa: %s", id, result.get_json())
>>>>>>> Stashed changes
    return result.get_json()
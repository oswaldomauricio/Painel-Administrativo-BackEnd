import sys
import os
from flask import jsonify
from models.cash_box_model import Cash_Box
from configs.connection import DBconnection
from datetime import datetime, timedelta
from decimal import Decimal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ResponseCashBox:
    def select(self):
        with DBconnection() as db:
            select_data = db.session.query(Cash_Box).all()
            return select_data

    def insert(self, id, data, num_doc, origem, tipo_operacao, valor, status, id_users, id_stores):
        with DBconnection() as db:
            insert_data = Cash_Box(ID=id, DATA=data, NUM_DOC=num_doc, ORIGEM=origem, TIPO_OPERACAO=tipo_operacao,
                                   VALOR=valor, STATUS=status, ID_USERS=id_users, ID_STORES=id_stores)
            db.session.add(insert_data)
            db.session.commit()

    def update(self, id, status):
        with DBconnection() as db:
            db.session.query(Cash_Box).filter(Cash_Box.ID == id).update({"STATUS": status})
            db.session.commit()


class CashBox_select_Controller:
    # pegar as informações da tabela f_caixa, criar uma função que calcule os valores de acordo com o status, e o tipo da operação.0
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def select_all_info_by_cashBox(self, id_loja, date_operacao):
        if not id_loja:
            return jsonify({"error": "O campo id_loja não foi informado.", 'status': 400})

        if not date_operacao:
            return jsonify({"error": "O campo de data não foi informado.", 'status': 400})

        try:
            data = self.response_CashBox.select()
            info_to_dict = [infos.to_dict() for infos in data]

            boxCash_return = [
                boxCash for boxCash in info_to_dict
                if boxCash.get('id_stores') == id_loja and boxCash.get('data') == date_operacao and boxCash.get('status') is True
            ]

            current_date = datetime.strptime(date_operacao, "%d/%m/%Y")
            previous_date = current_date - timedelta(days=1)
            previous_date_str = previous_date.strftime("%d/%m/%Y")

            # Buscar registros para a data anterior
            boxCash_previous_return = [
                boxCash for boxCash in info_to_dict
                if boxCash.get('id_stores') == id_loja and boxCash.get('data') == previous_date_str and boxCash.get('status') is True
            ]

            if boxCash_return:
                total_value_day = self.return_total_value_day(boxCash_return)
                previus_value = self.return_total_value_day(boxCash_previous_return)
                success_response = {
                    'Caixa': boxCash_return,
                    'Saldo': {
                        'Saldo do dia': total_value_day,
                        'Saldo do dia anterior': previus_value,
                        'Saldo total': total_value_day + previus_value
                    },
                    'status': 200
                }
                return jsonify(success_response)
            else:
                return jsonify({
                    'message': 'Nenhuma informação encontrada com os critérios fornecidos.',
                    'status': 404
                })

        except Exception as e:
            error_response = {
                "error": f"Ocorreu um erro: {str(e)}", 'status': 400}
            return jsonify(error_response)

    def return_total_value_day(self, caixa_data):
        total = 0.0
        try:
            for item in caixa_data:
                tipo_operacao = item.get('tipo_operacao')
                valor = item.get('valor', 0)

                valor = float(valor) if isinstance(valor, Decimal) else valor

                if tipo_operacao == 'ENTRADA':
                    total += valor
                elif tipo_operacao == 'SAIDA':
                    total -= valor

            return total
        except Exception as e:
            return jsonify({'error': f'Erro ao calcular o valor total: {str(e)}', 'status': 400})


class CashBox_insert_Controller:
    # pegar as informações da tabela f_caixa, criar uma função que calcule os valores de acordo com o status, e o tipo da operação.
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def insert_info_cashbox(self, id, id_loja, date_operacao, tipo_operacao, valor, status, numero_doc, origem, id_user):
        try:
            result = self.response_CashBox.insert(
                id, date_operacao, numero_doc, origem, tipo_operacao, valor, status, id_user, id_loja)
            return jsonify({'result': 'Registro inserido com sucesso.', 'status': 200})
        except Exception as e:
            return jsonify({'error': f'Erro ao inserir os dados: {str(e)}', 'status': 400})


class cashBox_delete_controller:
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox
        
    def delete_info_cashbox(self, id, status):
        try:
            self.response_CashBox.update(id, status)
            return jsonify({'result': 'Registro excluido com sucesso.', 'status': 200})
        except Exception as e:
            return jsonify({'error': f'Erro ao inserir os dados: {str(e)}', 'status': 400})

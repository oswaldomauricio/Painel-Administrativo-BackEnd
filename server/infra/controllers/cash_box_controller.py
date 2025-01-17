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

    def insert(self, id, data, num_doc, origem, tipo_operacao, valor, status, id_users, loja):
        with DBconnection() as db:
            insert_data = Cash_Box(ID=id, DATA=data, NUM_DOC=num_doc, ORIGEM=origem, TIPO_OPERACAO=tipo_operacao,
                                   VALOR=valor, STATUS=status, ID_USERS=id_users, STORE=loja)
            db.session.add(insert_data)
            db.session.commit()

    def update(self, id, status):
        with DBconnection() as db:
            db.session.query(Cash_Box).filter(
                Cash_Box.ID == id).update({"STATUS": status})
            db.session.commit()

class CashBox_select_Controller:
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def select_all_info_by_cashBox(self, loja, date_operacao):
        if not loja:
            return jsonify({"error": "O campo loja não foi informado.", 'status': 400})

        if not date_operacao:
            return jsonify({"error": "O campo de data não foi informado.", 'status': 400})

        try:
            data = self.response_CashBox.select()
            info_to_dict = [infos.to_dict() for infos in data]

            boxCash_return = [
                boxCash for boxCash in info_to_dict
                if boxCash.get('loja') == loja and boxCash.get('data') == date_operacao and boxCash.get('status') is True
            ]

            current_date = datetime.strptime(date_operacao, "%d/%m/%Y")
            previous_date = current_date - timedelta(days=1)
            previous_date_str = previous_date.strftime("%d/%m/%Y")

            boxCash_previous_return = [
                boxCash for boxCash in info_to_dict
                if boxCash.get('loja') == loja and boxCash.get('data') == previous_date_str and boxCash.get('status') is True
            ]

            if boxCash_return:
                total_value_day, total_entrada, total_saida = self.return_total_value_day(boxCash_return)
                previus_value = self.return_total_value_day(boxCash_previous_return)[0]
                success_response = {
                    'Caixa': boxCash_return,
                    'Saldo': {
                        'Saldo do dia': total_value_day,
                        'Saldo do dia anterior': previus_value,
                        'Saldo total': total_value_day + previus_value,
                        'entrada': total_entrada,
                        'saida': total_saida
                    },
                    'status': 200
                }
                return jsonify(success_response)
            else:
                return jsonify({
                    'error': 'Nenhuma informação encontrada com os critérios fornecidos.',
                    'status': 404
                })

        except Exception as e:
            error_response = {
                "error": f"Ocorreu um erro: {str(e)}", 'status': 400}
            return jsonify(error_response)

    def return_total_value_day(self, caixa_data):
        total = 0.0
        total_entrada = 0.0
        total_saida = 0.0
        try:
            for item in caixa_data:
                tipo_operacao = item.get('tipo_operacao')
                valor = item.get('valor', 0)

                valor = float(valor) if isinstance(valor, Decimal) else valor

                if tipo_operacao == 'ENTRADA':
                    total += valor
                    total_entrada += valor
                elif tipo_operacao == 'SAIDA':
                    total -= valor
                    total_saida += valor

            return total, total_entrada, total_saida
        except Exception as e:
            return jsonify({'error': f'Erro ao calcular o valor total: {str(e)}', 'status': 400})

class CashBox_insert_Controller:
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def insert_info_cashbox(self, id, loja, date_operacao, tipo_operacao, valor, status, numero_doc, origem, id_user):
        try:
            result = self.response_CashBox.insert(
                id, date_operacao, numero_doc, origem, tipo_operacao, valor, status, id_user, loja)

            info_caixa = {
                'id': id,
                'date_operacao': date_operacao,
                'numero_doc': numero_doc,
                'origem': origem,
                'tipo_operacao': tipo_operacao,
                'valor': valor,
                'status': status,
                'id_user': id_user,
                'loja': loja
            }

            json_info_caixa = jsonify(info_caixa)
            return jsonify({
                'result': 'Registro inserido com sucesso.',
                'status': 200,
                'caixas': info_caixa
            })
        except Exception as e:
            return jsonify({
                'error': f'Erro ao inserir os dados: {str(e)}',
                'status': 400
            })

class cashBox_delete_controller:
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def delete_info_cashbox(self, id, status):
        try:
            self.response_CashBox.update(id, status)
            return jsonify({'result': 'Registro excluido com sucesso.', 'status': 200})
        except Exception as e:
            return jsonify({'error': f'Erro ao inserir os dados: {str(e)}', 'status': 400})
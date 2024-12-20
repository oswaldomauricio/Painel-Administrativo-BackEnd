import sys

from flask import jsonify
from models.cash_box_model import Cash_Box
from configs.connection import DBconnection
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ResponseCashBox:
    def select(self):
        with DBconnection() as db:
            select_data = db.session.query(Cash_Box).all()
            return select_data

    def insert(self, data, num_doc, origem, tipo_operacao, valor, status, id_users, id_stores):
        with DBconnection() as db:
            insert_data = Cash_Box(DATA=data, NUM_DOC=num_doc, ORIGEM=origem, TIPO_OPERACAO=tipo_operacao,
                                   VALOR=valor, STATUS=status, ID_USERS=id_users, ID_STORES=id_stores)
            db.session.add(insert_data)
            db.session.commit()

    def delete(self, id):
        with DBconnection() as db:
            db.session.query(Cash_Box).filter(Cash_Box.ID == id).delete()
            db.session.commit()


class CashBoxController:
    # pegar as informações da tabela f_caixa, criar uma função que calcule os valores de acordo com o status, e o tipo da operação.
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def select_all_info_by_cashBox(self, id_loja, tipo_operacao):
        if not id_loja:
            error_response = {"error": "O campo id_loja não foi informado."}
            return jsonify(error_response)

        if not tipo_operacao:
            error_response = {
                "error": "O campo tipo de operação não foi informado."}
            return jsonify(error_response)

        try:
            data = self.response_CashBox.select()
            info_to_dict = [infos.to_dict() for infos in data]

            boxCash_return = [
                boxCash for boxCash in info_to_dict
                if boxCash.get('id_stores') == id_loja and boxCash.get('tipo_operacao') == tipo_operacao
            ]

            if boxCash_return:
                success_response = {'Caixa': boxCash_return, 'status': 200}
                return jsonify(success_response)
            else:
                not_found_response = {
                    'message': 'Nenhum caixa encontrado com os critérios fornecidos.', 'status': 404}
                return jsonify(not_found_response)

        except Exception as e:
            error_response = {"error": f"Ocorreu um erro: {str(e)}"}
            return jsonify(error_response)

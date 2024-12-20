
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.connection import DBconnection
from models.cash_box_model import Cash_Box

class ResponseCashBox:
    def select(self):
        with DBconnection() as db:
            select_data = db.session.query(Cash_Box).all()
            return select_data
    
    def insert(self, data, num_doc, origem, tipo_operacao, valor, status, id_users, id_stores):
        with DBconnection() as db:
            insert_data = Cash_Box(DATA = data, NUM_DOC = num_doc, ORIGEM = origem, TIPO_OPERACAO = tipo_operacao, VALOR = valor, STATUS = status, ID_USERS = id_users, ID_STORES = id_stores)
            db.session.add(insert_data)
            db.session.commit()

    def delete(self, id):
        with DBconnection() as db:
            db.session.query(Cash_Box).filter(Cash_Box.ID == id).delete()
            db.session.commit()


# class CashBoxController:
#     #pegar as informações da tabela f_caixa, criar uma função que calcule os valores de acordo com o status, e o tipo da operação.

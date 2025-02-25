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
    
    def get_caixa_by_id(id):
        with DBconnection() as db:
            return db.session.query(Cash_Box).filter_by(ID=id).first()

    def insert(self, id, data, num_doc, origem, tipo_operacao, valor, status, id_users, loja, tipo):
        with DBconnection() as db:
            insert_data = Cash_Box(ID=id, DATA=data, NUM_DOC=num_doc, ORIGEM=origem, TIPO_OPERACAO=tipo_operacao,
                                   VALOR=valor, STATUS=status, ID_USERS=id_users, STORE=loja, TIPO=tipo)
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
            # Converter data de string para datetime
            current_date = datetime.strptime(date_operacao, "%d/%m/%Y")
            data = self.response_CashBox.select()
            info_to_dict = [infos.to_dict() for infos in data]

            # Filtrar registros por loja
            records_for_store = [
                boxCash for boxCash in info_to_dict if boxCash.get('loja') == loja and boxCash.get('status') == 1
            ]

            if not records_for_store:
                return jsonify({
                    "error": "Nenhum registro encontrado para a loja especificada.",
                    "status": 404
                })

            # Ordenar registros por data para facilitar a busca
            records_for_store.sort(
                key=lambda x: datetime.strptime(x.get('data'), "%d/%m/%Y"))

            # Inicializar variáveis de saldo
            saldo_total = 0.0
            total_entrada = 0.0
            total_saida = 0.0

            boxCash_return = []
            for record in records_for_store:
                record_date = datetime.strptime(record.get('data'), "%d/%m/%Y")

                if record_date <= current_date:
                    # Atualizar saldo total com base em todos os registros até a data atual
                    tipo_operacao = record.get('tipo_operacao')
                    valor = record.get('valor', 0)
                    valor = float(valor) if isinstance(
                        valor, Decimal) else valor

                    if tipo_operacao == 'ENTRADA':
                        saldo_total += valor
                    elif tipo_operacao == 'SAIDA':
                        saldo_total -= valor

                if record_date == current_date:
                    # Calcular apenas os valores de entrada e saída do dia atual
                    tipo_operacao = record.get('tipo_operacao')
                    valor = record.get('valor', 0)
                    valor = float(valor) if isinstance(
                        valor, Decimal) else valor

                    if tipo_operacao == 'ENTRADA':
                        total_entrada += valor
                    elif tipo_operacao == 'SAIDA':
                        total_saida += valor

                    boxCash_return.append(record)

            # Resposta final
            success_response = {
                'Caixa': boxCash_return,
                'Saldo': {
                    'Saldo total': saldo_total,
                    'entrada': total_entrada,
                    'saida': total_saida
                },
                'status': 200
            }
            return jsonify(success_response)

        except Exception as e:
            error_response = {
                "error": f"Ocorreu um erro: {str(e)}", 'status': 400}
            return jsonify(error_response)

    def select_all_info_per_period(self, loja, data_inicial, data_final):
        if not loja:
            return jsonify({"error": "O campo loja não foi informado.", 'status': 400})

        if not data_inicial or not data_final:
            return jsonify({"error": "Os campos de data não foram informados.", 'status': 400})

        try:
            date_start = datetime.strptime(data_inicial, "%d/%m/%Y")
            date_end = datetime.strptime(data_final, "%d/%m/%Y")

            if date_start > date_end:
                return jsonify({"error": "A data inicial não pode ser maior que a data final.", 'status': 400})
        
            select_dados = self.response_CashBox.select()
            select_dados_to_dict = [infos.to_dict() for infos in select_dados]

            records_for_store = [
                boxCash for boxCash in select_dados_to_dict
                if boxCash.get('loja') == loja and boxCash.get('status') == 1
            ]

            if not records_for_store:
                return jsonify({
                    "error": "Nenhum registro encontrado para a loja especificada.",
                    "status": 404
                })

            filtered_records = [
                record for record in records_for_store
                if date_start <= datetime.strptime(record.get('data'), "%d/%m/%Y") <= date_end
            ]

            filtered_records.sort(key=lambda record: datetime.strptime(record.get('data'), "%d/%m/%Y"))

            saldo_total = 0.0
            total_entrada = 0.0
            total_saida = 0.0

            for record in filtered_records:
                valor = float(record.get('valor', 0)) if isinstance(record.get('valor'), Decimal) else record.get('valor')
                if record.get('tipo_operacao') == 'ENTRADA':
                    total_entrada += valor
                    saldo_total += valor
                elif record.get('tipo_operacao') == 'SAIDA':
                    total_saida += valor
                    saldo_total -= valor

            return jsonify({
                'Caixa': filtered_records,
                'Saldo': {
                    'Saldo total': saldo_total,
                    'entrada': total_entrada,
                    'saida': total_saida
                },
                'status': 200
            })
        except Exception as e:
            return jsonify({"error": f"Ocorreu um erro: {str(e)}", 'status': 400})



class CashBox_insert_Controller:
    def __init__(self, response_CashBox):
        self.response_CashBox = response_CashBox

    def insert_info_cashbox(self, id, loja, date_operacao, tipo_operacao, valor, status, numero_doc, origem, id_user, tipo):
        try:
            result = self.response_CashBox.insert(
                id, date_operacao, numero_doc, origem, tipo_operacao, valor, status, id_user, loja, tipo)

            info_caixa = {
                'id': id,
                'date_operacao': date_operacao,
                'numero_doc': numero_doc,
                'origem': origem,
                'tipo_operacao': tipo_operacao,
                'valor': valor,
                'status': status,
                'id_user': id_user,
                'loja': loja,
                'tipo': tipo
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

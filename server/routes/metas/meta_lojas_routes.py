from flask import Blueprint, request, jsonify
from infra.models.metas.meta_lojas_model import MetaLoja

meta_lojas_bp = Blueprint('meta_lojas', __name__)

# Rota GET por Nome e Senha
@meta_lojas_bp.route('/metas/lojas', methods=['POST'])
def get_meta_loja():
    data = request.get_json() 

    loja = data.get('loja')
    data_meta = data.get('data') 

    if not loja or not data_meta:
        return jsonify({'error': 'Campos "loja" e "data" são obrigatórios!'}), 400

    # Chama o método correto do controller (ex: buscar por loja e data)
    META_MENSAL = MetaLoja.buscar_metas_lojas_mes(loja, data_meta)
    META_SEMANAL = MetaLoja.buscar_metas_lojas_semanal(loja, data_meta)

    if META_SEMANAL and META_MENSAL:
        return jsonify({'meta_mensal': META_MENSAL, 'meta_semanal': META_SEMANAL, 'status': '200'  }), 200
    elif META_MENSAL:
        return jsonify({'meta_mensal': META_MENSAL, 'status': '200'  }), 200
    elif META_SEMANAL:
        return jsonify({'meta_semanal': META_SEMANAL, 'status': '200'  }), 200
    return jsonify({'error': 'Não existem metas para essa loja', 'status': '400' }), 400

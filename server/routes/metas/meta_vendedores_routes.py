from flask import Blueprint, request, jsonify
from infra.models.metas.meta_vendedores_model import MetaVendedores 

meta_vendedores_bp = Blueprint('meta_vendedores', __name__)

# Rota GET por Nome e Senha
@meta_vendedores_bp.route('/metas/vendedores/mes', methods=['POST'])
def get_meta_vendedores():
    data = request.get_json() 

    loja = data.get('loja')
    data_meta = data.get('data') 

    if not loja or not data_meta:
        return jsonify({'error': 'Campos "loja" e "data" são obrigatórios!', 'status': '400'}), 400

    META_VENDEDORES_MENSAL = MetaVendedores.buscar_metas_vendedores_mes(loja, data_meta)

    if META_VENDEDORES_MENSAL:
        return jsonify({'meta_vendedores_mensal': META_VENDEDORES_MENSAL, 'status': '200'  }), 200
    return jsonify({'error': 'Não existem metas para esse vendedor', 'status': '400' }), 400


@meta_vendedores_bp.route('/metas/vendedores/semanal', methods=['POST'])
def get_meta_vendedores_semanal():
    data = request.get_json() 

    nome_vendedor = data.get('nome_vendedor')
    data_meta = data.get('data') 

    if not nome_vendedor or not data_meta:
        return jsonify({'error': 'Nome do vendedor e data são obrigatórios!', 'status': '400'}), 400

    META_VENDEDORES_MENSAL = MetaVendedores.buscar_metas_vendedores_semanal(nome_vendedor, data_meta)

    if META_VENDEDORES_MENSAL:
        return jsonify({'meta_vendedores_semanal': META_VENDEDORES_MENSAL, 'status': '200'  }), 200
    
    return jsonify({'error': 'Não existem metas semanais para esse vendedor', 'status': '400' }), 400

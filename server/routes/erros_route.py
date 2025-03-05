from flask import Flask, jsonify
import logging

app = Flask(__name__)


@app.errorhandler(500)
def handle_internal_server_error():
    result = jsonify({
        "error": "Erro interno no servidor. Por favor, contate o suporte."
    }), 500
    logging.info("relatorio de caixa periodo (data inicial, data final e loja): %s", result)
    return result




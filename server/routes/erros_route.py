from flask import Flask, jsonify

app = Flask(__name__)


@app.errorhandler(500)
def handle_internal_server_error():
    return jsonify({
        "error": "Erro interno no servidor. Por favor, contate o suporte."
    }), 500




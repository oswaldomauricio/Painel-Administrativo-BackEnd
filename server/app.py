from flask import Flask  # jsonify, request
from infra.controllers.users_controller import UsersResponse
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')))

load_dotenv()

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DEBUG = os.getenv('DEBUG')

app = Flask(__name__)

response_users = UsersResponse()


@app.route('/usuario/<int:id>', methods=['GET'])
def value_entry(id):
    repo = UsersResponse()

    data = repo.select(id)

    dataDict = dict({
        'id': data[0].ID,
        'userName': data[0].NAME,
        'password': data[0].PASSWORD

    })
    return dataDict

@app.route('/usuario/<nome>/<password>', methods=['GET'])
def value_entry(nome, password):
    print(nome, password)
    repo = UsersResponse()

    data = repo.insert(nome, password)

    dataDict = dict({
        'id': data[0].ID,
        'userName': data[0].NAME,
        'password': data[0].PASSWORD

    })
    return dataDict

app.run(port=PORT, host=HOST, debug=True)

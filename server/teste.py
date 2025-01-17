from infra.controllers.stores_users_controller import StoreUsersController
from infra.controllers.users_controller import UsersResponse
from infra.controllers.stores_users_controller import ResponseStoreUser
from infra.controllers.cash_box_controller import CashBoxController
from infra.controllers.cash_box_controller import ResponseCashBox
from routes.cash_box_route import cashbox_bp
from flask import Flask



app = Flask(__name__)

#chamada das blueprints

app.register_blueprint(cashbox_bp)


# Inicialize as dependências
response_users = UsersResponse()
response_store_users = ResponseStoreUser()

# Instancie o controlador
store_users_controller = StoreUsersController(response_users, response_store_users)

# Use a função em outro contexto
def check_user_and_stores(name, password):

    result = store_users_controller.get_store_by_user(name, password)

    if result.get('status') == 200:
        print(f"User: {result['user']}")
        print(f"Stores: {result['stores']}")
    else:
        print(f"Error: {result['error']}")

# check_user_and_stores("oswaldo", "44844")

response_cashBox = ResponseCashBox()

# Instancie o controlador
CashBox_Controller = CashBoxController(response_cashBox)

# Use a função em outro contexto
def check_info_caixa(id_loja, tipo_operacao):
    with app.app_context():
        result = CashBox_Controller.select_all_info_by_cashBox(id_loja, tipo_operacao)
        print(result.get_json())  # Para extrair os dados JSON


check_info_caixa(1, 'ENTRADA')
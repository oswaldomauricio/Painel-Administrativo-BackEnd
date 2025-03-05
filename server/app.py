from flask import Flask
import logging
from flask_pydantic_spec import FlaskPydanticSpec
from routes.users_route import users_bp
from routes.store_users_route import store_users_bp
from routes.cash_box_route import cashbox_bp
from routes.metas.meta_lojas_routes import meta_lojas_bp 
from routes.metas.meta_vendedores_routes import meta_vendedores_bp 
import os

# Configuração de logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DEBUG = os.getenv('DEBUG')

app = Flask(__name__)
spec = FlaskPydanticSpec('Flask', title='API - NORTE AUTO PEÇAS')
spec.register(app)

#chamada das blueprints
app.register_blueprint(users_bp)
app.register_blueprint(store_users_bp)
app.register_blueprint(cashbox_bp)
app.register_blueprint(meta_lojas_bp)
app.register_blueprint(meta_vendedores_bp)


app.run(port=PORT, host=HOST, debug=True, load_dotenv=True, use_reloader=True)

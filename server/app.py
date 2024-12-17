from flask import Flask
from routes.users_route import users_bp
import os


PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DEBUG = os.getenv('DEBUG')

app = Flask(__name__)

#chamada das blueprints
app.register_blueprint(users_bp)

app.run(port=PORT, host=HOST, debug=True, load_dotenv=True, use_reloader=True)

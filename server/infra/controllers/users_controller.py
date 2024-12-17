
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.connection import DBconnection
from models.users_model import Users

class UsersResponse:
    def select(self, id):
        with DBconnection() as db:
            data = db.session.query(Users).filter(Users.ID == id)
            return data
        
    # def insert(self, nome, password):
    #     with DBconnection() as db:
    #         print('testandoo')
    #         insert_data = db.session.insert(Users).values(NAME = nome, PASSWORD = password)
    #         return insert_data
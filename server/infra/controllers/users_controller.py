
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.connection import DBconnection
from models.users_model import Users

class UsersResponse:
    def select(self):
        with DBconnection() as db:
            select_data = db.session.query(Users).all()
            return select_data
        
    def insert(self, nome, password):
        with DBconnection() as db:
            insert_data = Users(NAME = nome, PASSWORD = password)
            db.session.add(insert_data)
            db.session.commit()

    def update(self, nome, password, id):
        with DBconnection() as db:
            db.session.query(Users).filter(Users.ID == id).update({"NAME": nome, "PASSWORD": password})
            db.session.commit()

    def delete(self, id):
            with DBconnection() as db:
                db.session.query(Users).filter(Users.ID == id).delete()
                db.session.commit()

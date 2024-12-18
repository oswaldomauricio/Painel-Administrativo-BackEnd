
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.connection import DBconnection
from models.stores_users_model import Users_Stores

class ResponseStoreUser:
    def select(self):
        with DBconnection() as db:
            select_data = db.session.query(Users_Stores).all()
            return select_data
        
    def insert(self, loja, id_users, id):
        with DBconnection() as db:
            insert_data = Users_Stores(LOJA = loja, ID_USERS = id_users, ID = id)
            db.session.add(insert_data)
            db.session.commit()

    def update(self, loja, id_users):
        with DBconnection() as db:
            db.session.query(Users_Stores).filter(Users_Stores.ID_USERS == id_users, Users_Stores.LOJA == loja).update({"LOJA": loja})
            db.session.commit()

    def delete(self, id_users):
            with DBconnection() as db:
                db.session.query(Users_Stores).filter(Users_Stores.ID_USERS == id_users).delete()
                db.session.commit()
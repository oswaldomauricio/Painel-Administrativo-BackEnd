
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


class StoreUsersController:
    def __init__(self, response_users, response_store_users):
        self.response_users = response_users
        self.response_store_users = response_store_users

    def get_store_by_user(self, name, password):
        """Valida e retorna o usuário e suas lojas."""
        if not name or not password:
            return {'error': 'Nome e senha são obrigatórios!', 'status': 400}

        users = self.response_users.select()
        stores_users = self.response_store_users.select()

        users_to_dict = [user.to_dict() for user in users]
        stores_to_dict = [store.to_dict() for store in stores_users]

        for user in users_to_dict:
            if user['name'] == name and user['password'] == password:
                user_stores = [
                    store for store in stores_to_dict if store['id_users'] == user['id']
                ]
                return {'user': user, 'stores': user_stores, 'status': 200}

        # Caso nenhum usuário seja encontrado
        return {'error': 'Informações inválidas ou usuário não encontrado!', 'status': 404}

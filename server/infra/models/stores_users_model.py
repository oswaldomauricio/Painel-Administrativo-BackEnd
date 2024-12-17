import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs.base import Base

from sqlalchemy import Column, Integer, ForeignKey

class Users_Stores(Base):
    __tablename__ = 'lojas_users'

    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    LOJA = Column(Integer, nullable=False)
    ID_USERS = Column(Integer, ForeignKey("users.ID"))

    def __repr__(self):
        return f"<Users(Id={self.ID}, loja='{self.LOJA}', id_users='{self.ID_USERS}')>"

    def to_dict(self):
        return {
            "id": self.ID,
            "loja": self.LOJA,
            "id_users": self.ID_USERS,
        }

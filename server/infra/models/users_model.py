import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from configs.base import Base  
from sqlalchemy import Column, String, Integer

class Users(Base):
    __tablename__ = 'D_USERS'

    ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    NAME = Column(String, nullable=False)
    PASSWORD = Column(String, nullable=False)
    ROLE = Column(String)

    def __repr__(self):
        return f"[Id={self.ID}, Name='{self.NAME}', Password='{self.PASSWORD}, Role='{self.ROLE}']"

    def to_dict(self):
        return {
            "id": self.ID,
            "name": self.NAME,
            "password": self.PASSWORD,
            "role": self.ROLE
        }

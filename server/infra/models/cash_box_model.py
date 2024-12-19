from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Boolean
from configs.base import Base
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Cash_Box(Base):
    __tablename__ = 'F_CAIXA'

    ID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    DATA = Column(Date, nullable=False)
    NUM_DOC = Column(String, nullable=False)
    ORIGEM = Column(String, nullable=False)
    TIPO_OPERACAO = Column(String, nullable=False)
    VALOR = Column(Numeric, nullable=True)
    STATUS = Column(Boolean, nullable=True)
    ID_USERS = Column(Integer, ForeignKey("D_USERS.ID"))
    ID_STORE = Column(Integer, ForeignKey("D_USER_STORES"))

    def __repr__(self):
        return f"[id={self.ID}, data={self.DATA}, num_doc='{self.NUM_DOC}', origem='{self.ORIGEM}', tipo_operacao='{self.TIPO_OPERACAO}', valor={self.VALOR}, status={self.STATUS}, id_users={self.ID_USERS}, id_store={self.ID_STORE}]"

    def to_dict(self):
        return {
            "id": self.ID,
            "data": self.DATA,
            "num_doc": self.NUM_DOC,
            "origem": self.ORIGEM,
            "tipo_operacao": self.TIPO_OPERACAO,
            "valor": self.VALOR,
            "status": self.STATUS,
            "id_users": self.ID_USERS,
            "id_store": self.ID_STORE
        }

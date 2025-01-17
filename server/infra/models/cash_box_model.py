from sqlalchemy import Column, Integer, ForeignKey, Date, String, Numeric, Boolean
from configs.base import Base
import sys
import os
from datetime import datetime

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
    STORE = Column(Integer, nullable=True)

    @classmethod
    def parse_date(cls, date_str):
        """Convert date string to datetime object."""
        if isinstance(date_str, datetime):
            return date_str
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    raise ValueError("Date must be in DD/MM/YYYY or YYYY-MM-DD format")
        return date_str

    def __init__(self, **kwargs):
        if 'DATA' in kwargs:
            kwargs['DATA'] = self.parse_date(kwargs['DATA'])
        super().__init__(**kwargs)

    def __repr__(self):
        return f"[id={self.ID}, data={self.DATA}, num_doc='{self.NUM_DOC}', " \
               f"origem='{self.ORIGEM}', tipo_operacao='{self.TIPO_OPERACAO}', " \
               f"valor={self.VALOR}, status={self.STATUS}, id_users={self.ID_USERS}, " \
               f"loja='{self.STORE}']"

    def to_dict(self):
        formatted_date = self.DATA.strftime('%d/%m/%Y') if self.DATA else None
        return {
            "id": self.ID,
            "data": formatted_date,
            "num_doc": self.NUM_DOC,
            "origem": self.ORIGEM,
            "tipo_operacao": self.TIPO_OPERACAO,
            "valor": self.VALOR,
            "status": self.STATUS,
            "id_users": self.ID_USERS,
            "loja": self.STORE
        }
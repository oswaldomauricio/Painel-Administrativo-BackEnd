import os
from dotenv import load_dotenv
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBconnection:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBconnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not DBconnection._initialized:
            load_dotenv()
            
            self.PORTBD = os.getenv('PORTBD')
            self.HOSTBD = os.getenv('HOSTBD')
            self.SERVICENAME = os.getenv('SERVICENAME')
            self.USER = os.getenv('USER')
            self.PASSWORD = os.getenv('PASSWORD')

            try:
                cx_Oracle.init_oracle_client(
                    lib_dir=r'C:\instantclient-basic-windows.x64-23.6.0.24.10\instantclient_23_6'
                )
            except Exception as e:
                pass

            self.__connection_string = f'oracle+cx_oracle://{self.USER}:{self.PASSWORD}@{self.HOSTBD}:{self.PORTBD}/?service_name={self.SERVICENAME}'
            self.__engine = self.__create_database_engine()
            self.session = None
            DBconnection._initialized = True

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

# Criar uma instância global para ser usada em toda a aplicação
db_instance = DBconnection()
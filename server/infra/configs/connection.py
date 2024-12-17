import os
from dotenv import load_dotenv
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv() 

PORTBD = os.getenv('PORTBD')
INSTANTCLIENT = os.getenv('INSTANTCLIENT')
HOSTBD = os.getenv('HOSTBD')
SERVICENAME = os.getenv('SERVICENAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

cx_Oracle.init_oracle_client(
    lib_dir=INSTANTCLIENT)


class DBconnection:
    def __init__(self):
        self.__connection_string = f'oracle+cx_oracle://{USER}:{PASSWORD}@{HOSTBD}:{PORTBD}/?service_name={SERVICENAME}'
        self.__engine = self.__create_database_engine()
        self.session = None

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
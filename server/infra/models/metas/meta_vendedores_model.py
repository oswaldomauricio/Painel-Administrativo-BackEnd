from flask_pydantic_spec import FlaskPydanticSpec
from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import text
from infra.configs.connection import db_instance
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../')))


class MetaVendedores(Base):

    __tablename__ = 'COMISSAO'

    LOJA = Column(Integer, primary_key=True)
    UF = Column(String(2))
    DATA = Column(DateTime)
    META = Column(Numeric(10, 2))
    MES = Column(Integer)
    ANO = Column(Integer)
    TOTAL_VENDAS = Column(Integer)

    @classmethod
    def buscar_metas_vendedores_mes(cls, loja: int, data: str):
        """
        Busca as metas da loja no banco de dados.

        :param loja: Código da loja
        :param data: Data no formato 'DD/MM/YYYY'
        :return: Lista de resultados da consulta
        """
        meta_vendedores = text("""
            SELECT 
                    MV.COD_FILIAL,
                    MV.NOME_VENDEDOR,
                    EXTRACT(MONTH FROM MV.DATA_META) AS MES,
                    EXTRACT(YEAR FROM MV.DATA_META) AS ANO,     
                    MV.DATA_META AS DATA,
                    VENDAS.TOTAL_VENDAS,
                    MV.META,
                    TRUNC(((VENDAS.TOTAL_VENDAS / MV.META) * 100), 2) AS PERCENTUAL
                FROM ANALYTICS.METAS_VENDEDORES MV
                LEFT JOIN
                (
                    SELECT
                        CASE 
                            WHEN FUNC_USUARIO IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA'
                            WHEN FUNC_USUARIO IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'  
                            ELSE FUNC_USUARIO 
                        END AS NOME_VENDEDOR,
                        EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                        EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,     
                        SUM((CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END)) AS TOTAL_VENDAS
                    FROM VELIT.COMISSAO C
                    WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                    GROUP BY 
                        CASE 
                            WHEN FUNC_USUARIO IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA' 
                            WHEN FUNC_USUARIO IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'    
                            ELSE FUNC_USUARIO 
                        END,
                        EXTRACT(MONTH FROM C.COMIS_EMISSAO),
                        EXTRACT(YEAR FROM C.COMIS_EMISSAO)
                ) VENDAS
                ON VENDAS.NOME_VENDEDOR = 
                    CASE 
                        WHEN MV.NOME_VENDEDOR IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA' 
                        WHEN MV.NOME_VENDEDOR IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'    
                        ELSE MV.NOME_VENDEDOR 
                    END
                AND VENDAS.MES_META = EXTRACT(MONTH FROM MV.DATA_META) 
                AND VENDAS.ANO_META = EXTRACT(YEAR FROM MV.DATA_META)
                WHERE MV.COD_FILIAL = :loja -- Seleciona o número da filial
                AND MV.DATA_META = TO_DATE(:data, 'DD/MM/YYYY') -- Seleciona a data
                ORDER BY PERCENTUAL DESC
        """)

        with db_instance as db:
            result = db.session.execute(
                meta_vendedores, {"loja": loja, "data": data}).fetchall()

        metas_formatadas = []
        for row in result:
            meta_dict = {
                "LOJA": row[0],
                "VENDEDOR": row[1],
                "MES": row[2],
                "ANO": row[3],
                "DATA": row[4].strftime("%d/%m/%Y"),
                "TOTAL_VENDAS": float(row[5]) if row[5] is not None else 0.0,
                "META": float(row[6]) if row[6] is not None else 0.0,
                "PORCENTAGEM": float(row[7]) if row[7] is not None else 0.0
            }
            metas_formatadas.append(meta_dict)

        return metas_formatadas

    @classmethod
    def buscar_metas_vendedores_semanal(cls, nome_vendedor: str, data: str):
        """
        Busca as metas da loja no banco de dados.

        :param loja: Código da loja
        :param data: Data no formato 'DD/MM/YYYY'
        :return: Lista de resultados da consulta
        """
        meta_vendedores_semanal = text("""
            SELECT 
                A.COD_FILIAL,
                A.NOME_VENDEDOR,
                A.DATA,
                A.DATA_INICIO,
                A.DATA_FIM,
                A.META_SEMANAL,
                SUM(VENDAS.TOTAL_VENDAS) AS TOTAL_VENDAS_SEMANA,
                TRUNC(((SUM(VENDAS.TOTAL_VENDAS)/ A.META_SEMANAL)*100),2) AS PERCENTUAL
        FROM (
            SELECT 
            MV.COD_FILIAL,
            MV.NOME_VENDEDOR,
            MV.DATA_META AS DATA,
            MS.DATA_INICIO,
            MS.DATA_FIM,
            TRUNC(((MV.META / MD.QTD_DIAS) * MS.QTD_DIAS),2) AS META_SEMANAL 
    FROM ANALYTICS.METAS_VENDEDORES MV
    LEFT JOIN ANALYTICS.PARAMETRO_META_SEMANA MS ON MV.DATA_META = MS.DATA
    LEFT JOIN ANALYTICS.PARAMETRO_META_DIAS MD ON MD.DATA = MV.DATA_META
        ) A
        LEFT JOIN (
            SELECT
                C.FUNC_USUARIO AS NOME_VENDEDOR,
                TRUNC(C.COMIS_EMISSAO) AS DATA,
                (CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END) AS TOTAL_VENDAS
            FROM VELIT.COMISSAO C
            WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                ) VENDAS
            ON VENDAS.DATA BETWEEN A.DATA_INICIO AND A.DATA_FIM AND A.NOME_VENDEDOR = VENDAS.NOME_VENDEDOR
            WHERE A.NOME_VENDEDOR = :nome_vendedor  --------- Selecionar o Vendedor
            AND A.DATA = TO_DATE(:data, 'DD/MM/YYYY') ------------------- Selecionar a data de inicio
            GROUP BY
                A.COD_FILIAL,
                A.NOME_VENDEDOR,
                A.DATA,
                A.DATA_INICIO,
                A.DATA_FIM,
                A.META_SEMANAL
        """)

        with db_instance as db:
            result = db.session.execute(
                meta_vendedores_semanal, {"nome_vendedor": nome_vendedor, "data": data}).fetchall()

        metas_formatadas = []
        for row in result:
            meta_dict = {
                "LOJA": row[0],
                "VENDEDOR": row[1],
                "DATA": row[2].strftime("%d/%m/%Y"),
                "DATA_INICIO": row[3].strftime("%d/%m/%Y"),
                "DATA_FIM": row[4].strftime("%d/%m/%Y"),
                "META_SEMANAL": float(row[5]) if row[5] is not None else 0.0,
                "TOTAL_VENDAS": float(row[6]) if row[6] is not None else 0.0,
                "PORCENTAGEM": float(row[7]) if row[7] is not None else 0.0
            }
            metas_formatadas.append(meta_dict)

        return metas_formatadas

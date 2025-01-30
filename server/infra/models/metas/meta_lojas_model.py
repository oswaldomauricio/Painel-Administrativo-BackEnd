from flask_pydantic_spec import FlaskPydanticSpec
from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import text
from infra.configs.connection import db_instance
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../../')))


class MetaLoja(Base):

    __tablename__ = 'METAS_FILIAIS'

    cod_filial = Column(Integer, primary_key=True)
    uf = Column(String(2))
    data = Column(DateTime)
    meta = Column(Numeric(10, 2))
    mes = Column(Integer)
    ano_meta = Column(Integer)

    @classmethod
    def buscar_metas_lojas_mes(cls, loja: int, data: str):
        """
        Busca as metas da loja no banco de dados.

        :param loja: Código da loja
        :param data: Data no formato 'DD/MM/YYYY'
        :return: Lista de resultados da consulta
        """
        meta_mensal = text("""
            SELECT
            MF.UF,
            MF.COD_FILIAL,
            MF.DATA AS DATA_META,
            MES_META,
            VENDAS.TOTAL_VENDAS,
            MF.META,
            TRUNC(((VENDAS.TOTAL_VENDAS / MF.META) * 100),2) AS PERCENTUAL
        FROM (
            SELECT
                EMP_CODG AS COD_FILIAL,
                EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,
                SUM((CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END)) AS TOTAL_VENDAS
            FROM VELIT.COMISSAO C
            WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
            GROUP BY EMP_CODG, EXTRACT(MONTH FROM C.COMIS_EMISSAO), EXTRACT(YEAR FROM C.COMIS_EMISSAO)
        ) VENDAS
        LEFT JOIN ANALYTICS.METAS_FILIAIS MF ON VENDAS.COD_FILIAL = MF.COD_FILIAL AND VENDAS.MES_META = MF.MES AND VENDAS.ANO_META = MF.ANO_META
        WHERE VENDAS.COD_FILIAL = :loja and MF.DATA = TO_DATE(:data, 'DD/MM/YYYY')
        order by MF.COD_FILIAL, MES_META
        """)

        with db_instance as db:  # Use a instância única
            result = db.session.execute(
                meta_mensal, {"loja": loja, "data": data}).fetchall()

        metas_formatadas = []
        for row in result:
            meta_dict = {
                "UF": row[0],
                "LOJA": row[1],
                "DATA": row[2].strftime("%d/%m/%Y"),
                "MES_META": row[3],
                "TOTAL_VENDAS": float(row[4]) if row[4] is not None else 0.0,
                "META": float(row[5]) if row[5] is not None else 0.0,
                "PORCENTAGEM": float(row[6]) if row[6] is not None else 0.0
            }
            metas_formatadas.append(meta_dict)

        return metas_formatadas

    @classmethod
    def buscar_metas_lojas_semanal(cls, loja: int, data: str):
        """
            Busca as metas da loja na semana no banco de dados.

            :param loja: Código da loja
            :param data: Data no formato 'DD/MM/YYYY'
            :return: Lista de resultados da consulta
            """
        meta_semanal = text("""
                SELECT 
                    A.COD_FILIAL,
                    A.UF,
                    A.DATA,
                    A.DATA_INICIO,
                    A.DATA_FIM,
                    A.META_SEMANAL,
                    SUM(VENDAS.TOTAL_VENDAS) AS TOTAL_VENDAS_SEMANA,
                    TRUNC(((SUM(VENDAS.TOTAL_VENDAS) / A.META_SEMANAL) * 100), 2) AS PERCENTUAL
                FROM (
                    SELECT 
                    MF.COD_FILIAL,
                    MF.UF,
                    MF.MES,
                    MF.GERENTE,
                    MF.ANO_META,
                    MF.DATA,
                    MS.DATA_INICIO,
                    MS.DATA_FIM,
                    TRUNC(((MF.META / MD.QTD_DIAS) * MS.QTD_DIAS),2) AS META_SEMANAL  ---- DIMINUI O CALCULO DAS METAS SEMANAIS
                FROM ANALYTICS.METAS_FILIAIS MF
                LEFT JOIN ANALYTICS.PARAMETRO_META_SEMANA MS ON MF.DATA = MS.DATA
                LEFT JOIN ANALYTICS.PARAMETRO_META_DIAS MD ON MD.DATA = MF.DATA  ---- INCLUI ESSE LEFT JOIN PARA PEGAR AUTOMATICO A QUANTIDADE DE DIAS DO MES
                ) A
                LEFT JOIN (
                    SELECT
                        C.EMP_CODG AS COD_FILIAL,
                        TRUNC(C.COMIS_EMISSAO) AS DATA,
                        (CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END) AS TOTAL_VENDAS
                    FROM VELIT.COMISSAO C
                    WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                ) VENDAS
                ON VENDAS.DATA BETWEEN A.DATA_INICIO AND A.DATA_FIM AND A.COD_FILIAL = VENDAS.COD_FILIAL
                WHERE A.DATA = TO_DATE(:data, 'DD/MM/YYYY') -- Definir o mês
                AND A.COD_FILIAL = :loja -- Definir a loja
                GROUP BY
                    A.COD_FILIAL,
                    A.UF,
                    A.DATA,
                    A.DATA_INICIO,
                    A.DATA_FIM,
                    A.META_SEMANAL
                ORDER BY  
                    A.COD_FILIAL, A.DATA, A.DATA_INICIO
            """)

        with db_instance as db:  # Use a instância única
            result = db.session.execute(
                meta_semanal, {"loja": loja, "data": data}).fetchall()

            metas_formatadas = []
            for row in result:
                meta_dict = {
                    "UF": row[1],
                    "LOJA": row[0],
                    "DATA": row[2].strftime("%d/%m/%Y"),
                    "DATA_INICIO": row[3].strftime("%d/%m/%Y"),
                    "DATA_FIM": row[4].strftime("%d/%m/%Y"),
                    "META_SEMANAL": row[5],
                    "TOTAL_VENDAS": float(row[6]) if row[6] is not None else 0.0,
                    "PORCENTAGEM": float(row[7]) if row[7] is not None else 0.0
                }
                metas_formatadas.append(meta_dict)

            return metas_formatadas

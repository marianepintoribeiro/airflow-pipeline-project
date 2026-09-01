import logging
import os

import pandas as pd
import psycopg


logger = logging.getLogger(__name__)


def load(transformed_file):
    logger.info(
        "Iniciando carga no PostgreSQL. arquivo=%s",
        transformed_file,
    )

    dados = pd.read_csv(transformed_file)

    connection_params = {
        "host": os.environ["POSTGRES_HOST"],
        "port": os.environ["POSTGRES_PORT"],
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }

    query = """
        INSERT INTO vendas_transformadas (
            id_venda,
            quantidade,
            preco_unitario,
            valor_total
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id_venda)
        DO UPDATE SET
            quantidade = EXCLUDED.quantidade,
            preco_unitario = EXCLUDED.preco_unitario,
            valor_total = EXCLUDED.valor_total;
    """

    registros = [
        (
            int(row.id_venda),
            int(row.quantidade),
            float(row.preco_unitario),
            float(row.valor_total),
        )
        for row in dados.itertuples(index=False)
    ]

    logger.info(
        "Dados preparados para carga. registros=%s",
        len(registros),
    )

    with psycopg.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(query, registros)

    logger.info(
        "Carga no PostgreSQL concluída com sucesso. registros=%s",
        len(registros),
    )

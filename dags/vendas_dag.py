from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "vendas.csv")
TRANSFORMED_FILE = os.path.join(BASE_DIR, "data", "vendas_transformadas.csv")


def ingest():
    print("Iniciando ingestão dos dados...")

    dados = pd.read_csv(INPUT_FILE)

    print(f"{len(dados)} registros carregados.")
    print(dados.head())


def transform():
    print("Iniciando transformação dos dados...")

    dados = pd.read_csv(INPUT_FILE)

    dados["valor_total"] = (
        dados["quantidade"] * dados["preco_unitario"]
    )

    dados.to_csv(TRANSFORMED_FILE, index=False)

    print("Transformação concluída.")
    print(f"Arquivo gerado: {TRANSFORMED_FILE}")


def validate():
    print("Iniciando validação dos dados...")

    dados = pd.read_csv(TRANSFORMED_FILE)

    if dados.empty:
        raise ValueError("O arquivo não possui registros.")

    if dados["id_venda"].isnull().any():
        raise ValueError("Existem vendas sem ID.")

    if (dados["quantidade"] <= 0).any():
        raise ValueError("Existem quantidades inválidas.")

    if (dados["preco_unitario"] <= 0).any():
        raise ValueError("Existem preços unitários inválidos.")

    valores_calculados = (
    dados["quantidade"] * dados["preco_unitario"]
)

if not (dados["valor_total"] == valores_calculados).all():
    raise ValueError("Existem valores totais incorretos.")

    print(f"{len(dados)} registros validados com sucesso.")


with DAG(
    dag_id="pipeline_vendas",
    start_date=datetime(2026, 8, 21),
    schedule=None,
    catchup=False,
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

    validate_task = PythonOperator(
        task_id="validate",
        python_callable=validate,
    )

    ingest_task >> transform_task >> validate_task

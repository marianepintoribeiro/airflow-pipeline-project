from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv


def ingest():
    print("Iniciando ingestão dos dados...")
    
    with open("vendas.csv", "r", encoding="utf-8") as arquivo:
        dados = list(csv.DictReader(arquivo))
    
    print(f"{len(dados)} registros carregados.")


def transform():
    print("Transformando os dados...")
    print("Dados preparados para validação.")


def validate():
    print("Validando os dados...")
    print("Validação concluída com sucesso.")


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

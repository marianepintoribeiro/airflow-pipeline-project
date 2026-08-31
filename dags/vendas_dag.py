from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path

from src.ingestion import ingest
from src.transformation import transform
from src.validation import validate


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "vendas.csv"
TRANSFORMED_FILE = BASE_DIR / "data" / "vendas_transformadas.csv"


with DAG(
    dag_id="pipeline_vendas",
    start_date=datetime(2026, 8, 21),
    schedule=None,
    catchup=False,
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest,
        op_kwargs={
            "input_file": INPUT_FILE,
        },
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
        op_kwargs={
            "input_file": INPUT_FILE,
            "transformed_file": TRANSFORMED_FILE,
        },
    )

    validate_task = PythonOperator(
        task_id="validate",
        python_callable=validate,
        op_kwargs={
            "transformed_file": TRANSFORMED_FILE,
        },
    )

    ingest_task >> transform_task >> validate_task
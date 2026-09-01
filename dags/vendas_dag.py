from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path

from src.ingestion import ingest
from src.transformation import transform
from src.validation import validate
from src.load import load


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "vendas.csv"
TRANSFORMED_FILE = BASE_DIR / "data" / "vendas_transformadas.csv"

DEFAULT_ARGS = {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="pipeline_vendas",
    start_date=datetime(2026, 8, 21),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
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

    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
        op_kwargs={
            "transformed_file": TRANSFORMED_FILE,
        },
    )

    ingest_task >> transform_task >> validate_task >> load_task

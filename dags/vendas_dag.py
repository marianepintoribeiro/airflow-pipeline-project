from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import csv
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "vendas.csv")
TRANSFORMED_FILE = os.path.join(BASE_DIR, "data", "vendas_transformadas.csv")


def ingest():
    print("Iniciando ingestão dos dados...")

    with open(INPUT_FILE, "r", encoding="utf-8") as arquivo:
        dados = list(csv.DictReader(arquivo))

    print(f"{len(dados)} registros carregados.")


def transform():
    print("Iniciando transformação dos dados...")

    with open(INPUT_FILE, "r", encoding="utf-8") as arquivo:
        dados = list(csv.DictReader(arquivo))

    for venda in dados:
        quantidade = int(venda["quantidade"])
        preco_unitario = float(venda["preco_unitario"])

        venda["valor_total"] = quantidade * preco_unitario

    with open(TRANSFORMED_FILE, "w", newline="", encoding="utf-8") as arquivo:
        campos = [
            "id_venda",
            "data",
            "produto",
            "quantidade",
            "preco_unitario",
            "valor_total"
        ]

        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)

    print("Transformação concluída.")


def validate():
    print("Iniciando validação dos dados...")

    with open(TRANSFORMED_FILE, "r", encoding="utf-8") as arquivo:
        dados = list(csv.DictReader(arquivo))

    if len(dados) == 0:
        raise ValueError("O arquivo não possui registros.")

    for venda in dados:
        if not venda["id_venda"]:
            raise ValueError("Venda sem ID.")

        if int(venda["quantidade"]) <= 0:
            raise ValueError("Quantidade inválida.")

        if float(venda["preco_unitario"]) <= 0:
            raise ValueError("Preço unitário inválido.")

        valor_calculado = (
            int(venda["quantidade"]) *
            float(venda["preco_unitario"])
        )

        if float(venda["valor_total"]) != valor_calculado:
            raise ValueError("Valor total inválido.")

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

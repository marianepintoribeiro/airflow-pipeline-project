import pandas as pd


def ingest(input_file):
    print("Iniciando ingestão dos dados...")

    dados = pd.read_csv(input_file)

    print(f"{len(dados)} registros carregados.")
    print(dados.head())
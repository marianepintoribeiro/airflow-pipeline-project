import pandas as pd


def transform(input_file, transformed_file):
    print("Iniciando transformação dos dados...")

    dados = pd.read_csv(input_file)

    dados["valor_total"] = (
        dados["quantidade"] * dados["preco_unitario"]
    )

    dados.to_csv(transformed_file, index=False)

    print("Transformação concluída.")
    print(f"Arquivo gerado: {transformed_file}")
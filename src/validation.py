import pandas as pd


def validate(transformed_file):
    print("Iniciando validação dos dados...")

    dados = pd.read_csv(transformed_file)

    if dados.empty:
        raise ValueError("O arquivo não possui registros.")

    if dados["id_venda"].isnull().any():
        raise ValueError("Existem vendas sem ID.")

    if dados["id_venda"].duplicated().any():
        raise ValueError("Existem IDs de venda duplicados.")

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
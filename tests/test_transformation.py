import pandas as pd

from src.transformation import transform


def test_transform_calcula_valor_total(tmp_path):
    input_file = tmp_path / "vendas.csv"
    output_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
        }
    )

    dados.to_csv(input_file, index=False)

    transform(input_file, output_file)

    resultado = pd.read_csv(output_file)

    assert resultado["valor_total"].tolist() == [20.0, 15.0]

def test_transform_e_idempotente(tmp_path):
    input_file = tmp_path / "vendas.csv"
    output_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
        }
    )

    dados.to_csv(input_file, index=False)

    transform(input_file, output_file)
    primeira_execucao = pd.read_csv(output_file)

    transform(input_file, output_file)
    segunda_execucao = pd.read_csv(output_file)

    pd.testing.assert_frame_equal(
        primeira_execucao,
        segunda_execucao,
    )
    
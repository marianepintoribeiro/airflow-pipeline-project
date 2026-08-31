import pandas as pd
import pytest

from src.validation import validate


def test_validate_rejeita_id_duplicado(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 1],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
            "valor_total": [20.0, 15.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="Existem IDs de venda duplicados."
    ):
        validate(transformed_file)

def test_validate_rejeita_id_nulo(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, None],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
            "valor_total": [20.0, 15.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="Existem vendas sem ID."
    ):
        validate(transformed_file)

def test_validate_rejeita_quantidade_invalida(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 0],
            "preco_unitario": [10.0, 5.0],
            "valor_total": [20.0, 0.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="Existem quantidades inválidas."
    ):
        validate(transformed_file)

def test_validate_rejeita_preco_unitario_invalido(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 0.0],
            "valor_total": [20.0, 0.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="Existem preços unitários inválidos."
    ):
        validate(transformed_file)

def test_validate_rejeita_arquivo_vazio(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        columns=[
            "id_venda",
            "quantidade",
            "preco_unitario",
            "valor_total",
        ]
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="O arquivo não possui registros."
    ):
        validate(transformed_file)

def test_validate_rejeita_valor_total_incorreto(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
            "valor_total": [20.0, 999.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    with pytest.raises(
        ValueError,
        match="Existem valores totais incorretos."
    ):
        validate(transformed_file)

def test_validate_aceita_dados_validos(tmp_path):
    transformed_file = tmp_path / "vendas_transformadas.csv"

    dados = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "quantidade": [2, 3],
            "preco_unitario": [10.0, 5.0],
            "valor_total": [20.0, 15.0],
        }
    )

    dados.to_csv(transformed_file, index=False)

    validate(transformed_file)
    
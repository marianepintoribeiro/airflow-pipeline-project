import logging

import pandas as pd


logger = logging.getLogger(__name__)


def transform(input_file, transformed_file):
    logger.info(
        "Iniciando transformação dos dados. entrada=%s saída=%s",
        input_file,
        transformed_file,
    )

    dados = pd.read_csv(input_file)

    dados["valor_total"] = (
        dados["quantidade"] * dados["preco_unitario"]
    )

    dados.to_csv(transformed_file, index=False)

    logger.info(
        "Transformação concluída com sucesso. registros=%s colunas=%s",
        len(dados),
        len(dados.columns),
    )

import logging

import pandas as pd


logger = logging.getLogger(__name__)


def ingest(input_file):
    logger.info("Iniciando ingestão dos dados. arquivo=%s", input_file)

    dados = pd.read_csv(input_file)

    logger.info(
        "Ingestão concluída com sucesso. registros=%s colunas=%s",
        len(dados),
        len(dados.columns),
    )

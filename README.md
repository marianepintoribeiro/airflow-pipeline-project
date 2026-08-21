# Airflow Pipeline Project

Projeto de estudo em Engenharia de Dados utilizando Apache Airflow.

## Objetivo

Criar uma pipeline de dados simples para processar informações de vendas.

A pipeline será composta por três etapas:

1. Ingest — leitura dos dados de vendas
2. Transform — transformação dos dados
3. Validate — validação dos dados

## Estrutura do projeto

```text
airflow-pipeline-project/
│
├── dags/
│   └── pipeline_dados.py
│
├── data/
│   └── vendas.csv
│
├── README.md
└── requirements.txt

# Airflow Pipeline Project

Projeto de estudo em Engenharia de Dados utilizando Apache Airflow para criação de uma pipeline simples de processamento de dados de vendas.

## Objetivo

O objetivo deste projeto é demonstrar a construção de uma pipeline de dados utilizando Apache Airflow.

A pipeline possui três etapas principais:

1. **Ingest** — leitura dos dados de vendas a partir de um arquivo CSV.
2. **Transform** — transformação dos dados e cálculo do valor total de cada venda.
3. **Validate** — validação da qualidade e consistência dos dados processados.

## Pipeline

O fluxo de execução da DAG é:

```text
vendas.csv
    │
    ▼
  Ingest
    │
    ▼
 Transform
    │
    ▼
 Validate
    │
    ▼
vendas_transformadas.csv
```

A transformação calcula o valor total de cada venda utilizando:

```text
valor_total = quantidade × preco_unitario
```

## Validações

A etapa de validação verifica:

* Se existem registros no arquivo.
* Se cada venda possui um ID.
* Se a quantidade é maior que zero.
* Se o preço unitário é maior que zero.
* Se o valor total foi calculado corretamente.

Caso alguma validação falhe, a task gera um erro e a execução da pipeline é interrompida.

## Estrutura do projeto

```text
airflow-pipeline-project/
│
├── dags/
│   ├── pipeline_dados.py
│   └── vendas_dag.py
│
├── data/
│   └── vendas.csv
│
├── README.md
│
└── requirements.txt
```

## Tecnologias utilizadas

* Python
* Apache Airflow
* CSV
* GitHub

## DAG

A DAG principal do projeto é:

```text
pipeline_vendas
```

Ela contém três tasks:

```text
ingest → transform → validate
```

## Dados

O arquivo `vendas.csv` contém informações de vendas, incluindo:

* ID da venda
* Data
* Produto
* Quantidade
* Preço unitário

A pipeline utiliza esses dados para gerar informações derivadas e realizar validações de qualidade.

## Status do projeto

Projeto desenvolvido para fins de estudo e portfólio em Engenharia de Dados.


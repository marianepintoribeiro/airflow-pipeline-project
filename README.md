# Airflow Sales Data Pipeline

Pipeline de dados desenvolvida em **Python, Pandas e Apache Airflow** para ingestão, transformação e validação de dados de vendas.

Este projeto foi desenvolvido como parte de um portfólio de estudos em **Engenharia de Dados**, com foco em conceitos fundamentais de pipelines, orquestração de tarefas e qualidade de dados.

## Objetivo

O objetivo do projeto é construir uma pipeline simples capaz de:

* Ler dados de vendas a partir de um arquivo CSV;
* Transformar os dados utilizando Pandas;
* Calcular o valor total de cada venda;
* Validar a qualidade dos dados processados;
* Orquestrar as etapas utilizando Apache Airflow.

## Arquitetura

O fluxo da pipeline é:

```text
                    vendas.csv
                        │
                        ▼
                   ┌─────────┐
                   │ INGEST  │
                   └────┬────┘
                        │
                        ▼
                  ┌───────────┐
                  │ TRANSFORM │
                  └─────┬─────┘
                        │
                        ▼
             vendas_transformadas.csv
                        │
                        ▼
                  ┌──────────┐
                  │ VALIDATE │
                  └──────────┘
```

### Fluxo de processamento

**1. Ingest**

A task `ingest` realiza a leitura do arquivo `vendas.csv` utilizando Pandas.

**2. Transform**

A task `transform` calcula o valor total de cada venda:

```text
valor_total = quantidade × preco_unitario
```

O resultado é salvo em um novo arquivo chamado `vendas_transformadas.csv`.

**3. Validate**

A task `validate` verifica a qualidade dos dados processados, garantindo que:

* O arquivo possui registros;
* Todas as vendas possuem um ID;
* A quantidade é maior que zero;
* O preço unitário é maior que zero;
* O valor total foi calculado corretamente.

## DAG

A DAG principal do projeto é:

```text
pipeline_vendas
```

As tasks são executadas na seguinte ordem:

```text
ingest → transform → validate
```

Essa dependência garante que a transformação só seja executada após a ingestão e que a validação ocorra após a transformação.

## Dados

O arquivo de entrada `vendas.csv` contém dados fictícios de vendas com as seguintes colunas:

| Coluna           | Descrição                       |
| ---------------- | ------------------------------- |
| `id_venda`       | Identificador da venda          |
| `data`           | Data da venda                   |
| `produto`        | Produto vendido                 |
| `quantidade`     | Quantidade de produtos vendidos |
| `preco_unitario` | Preço unitário do produto       |

A transformação adiciona a coluna:

| Coluna        | Descrição            |
| ------------- | -------------------- |
| `valor_total` | Valor total da venda |

## Tecnologias utilizadas

* **Python** — linguagem utilizada no desenvolvimento da pipeline;
* **Pandas** — leitura e transformação dos dados;
* **Apache Airflow** — orquestração das tarefas;
* **CSV** — formato dos dados de entrada e saída;
* **GitHub** — versionamento e documentação do projeto.

## Estrutura do projeto

```text
airflow-pipeline-project/
│
├── dags/
│   └── vendas_dag.py
│
├── data/
│   └── vendas.csv
│
├── README.md
│
└── requirements.txt
```

## Resultado esperado

A pipeline deve gerar um arquivo:

```text
data/vendas_transformadas.csv
```

Esse arquivo deverá conter os dados originais acrescidos da coluna `valor_total`.

Para os dados utilizados neste projeto, o valor total esperado das vendas é:

```text
R$ 26.390,00
```

## Status do projeto

🟡 **Em desenvolvimento**

O projeto está sendo desenvolvido como parte de um portfólio de Engenharia de Dados.

As próximas etapas incluem execução da DAG em um ambiente com Apache Airflow, testes do pipeline e validação dos arquivos gerados.

## Aprendizados

Este projeto permite praticar conceitos fundamentais de Engenharia de Dados, incluindo:

* Construção de pipelines;
* Orquestração com Apache Airflow;
* Manipulação de dados com Pandas;
* Transformação de dados;
* Validação de qualidade de dados;
* Organização de projetos;
* Versionamento com GitHub.


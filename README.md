# Airflow Sales Data Pipeline

Pipeline batch de dados de vendas desenvolvido em **Python** e orquestrado com **Apache Airflow**, implementando ingestão, transformação, validação de qualidade e persistência idempotente em **PostgreSQL**.

O projeto simula um fluxo de Engenharia de Dados no qual dados brutos em CSV são processados por etapas independentes e orquestradas. A solução incorpora **Pandas, PostgreSQL, Docker, pytest e GitHub Actions**, além de mecanismos de validação, reprocessamento seguro, logging contextual e testes automatizados.

## Objetivo

Construir um pipeline de dados reproduzível e testável capaz de:

- ingerir dados de vendas a partir de um arquivo CSV;
- aplicar transformações utilizando Pandas;
- validar regras de qualidade antes da persistência;
- carregar os dados processados em PostgreSQL;
- permitir reprocessamento sem duplicação de registros;
- orquestrar as etapas com Apache Airflow;
- executar testes automatizados com pytest;
- validar alterações automaticamente por meio de CI com GitHub Actions;
- executar os principais componentes da solução em ambiente containerizado com Docker.

## Arquitetura

O pipeline segue o fluxo:

```text
                         vendas.csv
                             │
                             ▼
                      ┌────────────┐
                      │   INGEST   │
                      └─────┬──────┘
                            │
                            ▼
                      ┌────────────┐
                      │ TRANSFORM  │
                      └─────┬──────┘
                            │
                            ▼
                vendas_transformadas.csv
                            │
                            ▼
                      ┌────────────┐
                      │  VALIDATE  │
                      └─────┬──────┘
                            │
                            ▼
                      ┌────────────┐
                      │    LOAD    │
                      └─────┬──────┘
                            │
                            ▼
                      PostgreSQL
                 vendas_transformadas
```

O **Apache Airflow** controla a ordem e a execução das etapas:

```text
ingest → transform → validate → load
```

A separação das responsabilidades permite que cada etapa seja desenvolvida, testada e observada individualmente.

## Fluxo do pipeline

### 1. Ingest

A etapa `ingest` lê o arquivo de origem `data/vendas.csv` utilizando Pandas e registra informações sobre o processamento, como quantidade de registros e colunas.

### 2. Transform

A etapa `transform` aplica a regra de negócio:

```text
valor_total = quantidade × preco_unitario
```

O resultado é persistido em `data/vendas_transformadas.csv`. A escrita determinística do arquivo permite sua sobrescrita durante reprocessamentos, evitando acúmulo de registros no artefato intermediário.

### 3. Validate

Antes da carga no banco, a etapa `validate` verifica regras de qualidade relacionadas a:

- arquivo vazio;
- IDs ausentes;
- IDs duplicados;
- quantidades inválidas;
- preços unitários inválidos;
- inconsistências no cálculo de `valor_total`.

Caso alguma regra seja violada, uma exceção é lançada e propagada para a orquestração, impedindo que dados inválidos avancem para a etapa de carga.

### 4. Load

Após a validação, a etapa `load` persiste os dados na tabela `vendas_transformadas` do PostgreSQL.

A carga utiliza uma estratégia de **upsert** baseada em `id_venda`:

```sql
ON CONFLICT (id_venda)
DO UPDATE
```

Com isso, o mesmo conjunto de dados pode ser reprocessado sem gerar duplicação de vendas na tabela.


## Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| **Python 3.12** | Desenvolvimento das etapas do pipeline |
| **Pandas** | Leitura, transformação e validação dos dados |
| **Apache Airflow 3.3.1** | Orquestração das etapas do pipeline |
| **PostgreSQL 16** | Persistência dos dados processados |
| **psycopg 3** | Conexão e operações entre Python e PostgreSQL |
| **pytest** | Testes automatizados de transformação e qualidade dos dados |
| **Docker** | Construção de ambiente reproduzível para execução do Airflow |
| **Docker Compose** | Orquestração local dos serviços Airflow e PostgreSQL |
| **GitHub Actions** | Integração contínua para execução automática da suíte de testes |
| **Git / GitHub** | Versionamento, colaboração e documentação do projeto |

## Estrutura do projeto

```text
airflow-pipeline-project/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── dags/
│   └── vendas_dag.py
│
├── data/
│   ├── vendas.csv
│   └── vendas_transformadas.csv
│
├── sql/
│   └── init.sql
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── transformation.py
│   ├── validation.py
│   └── load.py
│
├── tests/
│   ├── test_transformation.py
│   └── test_validation.py
│
├── .dockerignore
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

A organização separa responsabilidades entre orquestração, lógica de negócio, testes, infraestrutura e configuração do ambiente.

## Data Quality

A etapa de validação funciona como uma barreira antes da persistência no banco de dados.

As seguintes regras são verificadas:

| Regra | Comportamento esperado |
|---|---|
| Arquivo sem registros | Interrompe o pipeline |
| `id_venda` ausente | Interrompe o pipeline |
| `id_venda` duplicado | Interrompe o pipeline |
| `quantidade <= 0` | Interrompe o pipeline |
| `preco_unitario <= 0` | Interrompe o pipeline |
| `valor_total` inconsistente | Interrompe o pipeline |
| Dados válidos | Permite continuidade para a carga |

As validações lançam exceções explícitas quando encontram inconsistências. Isso permite que o Airflow registre a falha da task e preserve o traceback para investigação.

## Testes automatizados

O projeto utiliza **pytest** para validar comportamentos críticos das etapas de transformação e validação.

A suíte atual possui **9 testes automatizados**, cobrindo:

- cálculo correto de `valor_total`;
- reprocessamento idempotente da transformação;
- arquivo vazio;
- ID ausente;
- ID duplicado;
- quantidade inválida;
- preço unitário inválido;
- valor total incorreto;
- cenário válido.

Os testes utilizam arquivos temporários por meio de `tmp_path`, reduzindo dependência de estado compartilhado entre execuções.

Execução da suíte:

```bash
python -m pytest
```

Resultado validado:

```text
9 passed
```

## Idempotência e reprocessamento

O pipeline foi desenvolvido para permitir reprocessamentos sem gerar duplicação dos dados.

Na camada de arquivo, a transformação produz `vendas_transformadas.csv` de forma determinística, sobrescrevendo o resultado anterior em vez de acrescentar novos registros.

Na camada de persistência, `id_venda` é definido como chave primária no PostgreSQL e a carga utiliza uma operação de **upsert**:

```sql
ON CONFLICT (id_venda)
DO UPDATE SET
    quantidade = EXCLUDED.quantidade,
    preco_unitario = EXCLUDED.preco_unitario,
    valor_total = EXCLUDED.valor_total;
```

Em um teste de reprocessamento do mesmo conjunto de dados, a tabela permaneceu com **10 registros após a segunda execução**, demonstrando que a estratégia evita duplicação nesse cenário.

A DAG também possui uma política de retry configurada para até duas novas tentativas, com intervalo de um minuto entre elas.

## Persistência com PostgreSQL

Os dados validados são persistidos no PostgreSQL na tabela:

```text
vendas_transformadas
```

A estrutura é criada automaticamente a partir de `sql/init.sql` na inicialização de um novo volume de dados do PostgreSQL.

```sql
CREATE TABLE IF NOT EXISTS vendas_transformadas (
    id_venda INTEGER PRIMARY KEY,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL
);
```

A conexão entre a aplicação e o banco é realizada com **psycopg**, utilizando parâmetros fornecidos por variáveis de ambiente.

No ambiente Docker Compose, os dados de negócio são armazenados em um volume dedicado do PostgreSQL, separado do estado utilizado pelo Airflow.

## Docker e ambiente containerizado

O projeto utiliza uma imagem baseada em **Apache Airflow 3.3.1 com Python 3.12**.

O `Dockerfile` instala o projeto como pacote Python dentro da imagem e prepara o diretório utilizado pelo Airflow com as permissões necessárias para execução como usuário não-root.

O `compose.yaml` define dois serviços principais:

```text
Airflow ──────────► PostgreSQL
   │                    │
   ▼                    ▼
airflow_state       postgres_data
```

- `airflow_state`: persiste o estado local utilizado pelo Airflow;
- `postgres_data`: persiste os dados de negócio armazenados no PostgreSQL.

O `.dockerignore` reduz o contexto enviado durante o build, excluindo artefatos que não precisam fazer parte da imagem, como ambiente virtual, metadados do Git e caches Python.

Durante a otimização do ambiente, o contexto de build foi reduzido de aproximadamente **386 MB para 2 KB**, diminuindo o tempo observado de build de aproximadamente **84 segundos para 9 segundos**.

## Logging e observabilidade

As etapas do pipeline utilizam o módulo `logging` do Python para registrar eventos relevantes da execução.

Os logs incluem informações como:

- início e conclusão de cada etapa;
- arquivos de entrada e saída;
- quantidade de registros processados;
- quantidade de colunas;
- preparação dos registros para carga;
- conclusão da persistência no PostgreSQL.

Em situações de erro de validação, a exceção é propagada para o Airflow, permitindo que a task seja marcada como falha e que o traceback seja preservado para investigação.

## Integração contínua com GitHub Actions

O projeto possui um workflow de **Continuous Integration (CI)** configurado em:

```text
.github/workflows/ci.yml
```

O workflow é acionado em:

```text
push → main
pull_request → main
```

A execução provisiona **Python 3.12**, instala o projeto e suas dependências de desenvolvimento e executa:

```bash
python -m pytest
```

A suíte com **9 testes** foi executada com sucesso em um runner do GitHub Actions.

O comportamento do CI também foi validado por meio de um Pull Request temporário: um teste propositalmente inválido fez o workflow falhar e, após a correção, uma nova execução retornou ao estado de sucesso.

Atualmente, o CI automatiza a suíte de testes unitários do projeto. A execução end-to-end envolvendo Airflow, Docker e PostgreSQL não faz parte desse workflow.


## Como executar

### Pré-requisitos

Para execução containerizada, é necessário ter:

- Docker;
- Docker Compose.

### 1. Clonar o repositório

```bash
git clone https://github.com/marianepintoribeiro/airflow-pipeline-project.git
cd airflow-pipeline-project
```

### 2. Construir as imagens

```bash
docker compose build
```

### 3. Inicializar os serviços

```bash
docker compose up -d
```

O PostgreSQL é inicializado com a estrutura definida em `sql/init.sql`, enquanto o serviço do Airflow executa a preparação do seu ambiente.

### 4. Executar a DAG para teste

```bash
docker compose run --rm airflow \
  bash -c "airflow db migrate && airflow dags test pipeline_vendas 2026-09-01"
```

### 5. Consultar os dados persistidos

```bash
docker compose exec postgres \
  psql -U airflow -d vendas \
  -c "SELECT * FROM vendas_transformadas ORDER BY id_venda;"
```

### 6. Executar os testes automatizados

No ambiente Python com as dependências de desenvolvimento instaladas:

```bash
python -m pytest
```

## Resultados validados

A implementação foi validada em diferentes camadas do projeto:

| Validação | Resultado observado |
|---|---|
| Execução completa da DAG | `success` |
| Registros processados | 10 |
| Persistência no PostgreSQL | 10 registros |
| Reprocessamento do mesmo conjunto | 10 registros, sem duplicação |
| Testes automatizados | 9 testes aprovados |
| CI em código válido | sucesso |
| CI com falha proposital | falha detectada |
| CI após correção | sucesso |
| Build Docker após otimização | contexto reduzido de ~386 MB para ~2 KB |

## Decisões de engenharia

### Separação de responsabilidades

A lógica do pipeline foi dividida em módulos independentes de ingestão, transformação, validação e carga. A DAG fica responsável principalmente pela orquestração dessas funções, reduzindo o acoplamento entre regra de processamento e ferramenta de orquestração.

### Validação antes da persistência

As regras de qualidade são executadas antes da etapa de carga. Dessa forma, registros que violam as condições definidas não seguem para o PostgreSQL.

### Carga idempotente

A combinação de chave primária em `id_venda` e `ON CONFLICT ... DO UPDATE` permite reprocessar o mesmo conjunto de vendas sem inserir registros duplicados nesse cenário.

### Estado de orquestração separado dos dados de negócio

O ambiente Docker utiliza volumes distintos para o estado local do Airflow e para o PostgreSQL. Essa separação evita tratar metadados da ferramenta de orquestração como dados da aplicação.

### Testabilidade

A lógica de transformação e validação foi mantida em módulos Python separados da DAG. Isso permite executar testes com pytest sem depender da inicialização completa do Airflow.

### Dependências de desenvolvimento

As dependências necessárias aos testes são declaradas separadamente como dependências de desenvolvimento no `pyproject.toml`, enquanto as dependências utilizadas pela aplicação permanecem na configuração principal do projeto.

### Integração contínua

O GitHub Actions executa os testes automaticamente em alterações destinadas à branch principal, fornecendo um sinal automático de regressão antes da integração de mudanças.

## Limitações atuais

Este projeto representa uma implementação de portfólio executada em ambiente local/containerizado. Algumas características de uma arquitetura de produção não fazem parte do escopo atual:

- o dataset utilizado é pequeno e fictício;
- a origem dos dados é um arquivo CSV local;
- o Airflow utiliza configuração local para seus metadados;
- o CI atual executa testes automatizados, mas não testes de integração end-to-end com PostgreSQL e Airflow;
- as credenciais presentes no Docker Compose são destinadas exclusivamente ao ambiente local de desenvolvimento;
- não há integração com armazenamento em nuvem, data warehouse ou ferramentas externas de monitoramento.

## Próximos passos

Possíveis evoluções técnicas incluem:

- adicionar testes de integração para a carga no PostgreSQL;
- validar o import da DAG automaticamente no CI;
- adicionar execução end-to-end ao pipeline de CI;
- externalizar configurações e credenciais do ambiente;
- adicionar uma camada de armazenamento ou processamento em cloud;
- expandir o dataset e os cenários de Data Quality;
- adicionar monitoramento e alertas para falhas do pipeline.

## Principais aprendizados

O desenvolvimento deste projeto envolveu mais do que a implementação das transformações. Ao longo da evolução da solução foram trabalhados conceitos de:

- modularização de pipelines de dados;
- orquestração com Apache Airflow;
- Data Quality e tratamento de falhas;
- persistência relacional com PostgreSQL;
- idempotência e reprocessamento;
- testes automatizados;
- containerização e persistência com volumes;
- gerenciamento de dependências;
- logging e diagnóstico de falhas;
- integração contínua com GitHub Actions;
- versionamento e evolução incremental da arquitetura.

O projeto demonstra a evolução de um pipeline baseado em arquivos para uma solução orquestrada, testável, containerizada e com persistência em banco de dados.


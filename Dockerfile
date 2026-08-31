FROM apache/airflow:3.3.1-python3.12

USER root

RUN mkdir -p /opt/airflow/state \
    && chown -R airflow:root /opt/airflow/state

USER airflow

COPY --chown=airflow:root . /opt/airflow/project

RUN pip install --no-cache-dir -e "/opt/airflow/project"

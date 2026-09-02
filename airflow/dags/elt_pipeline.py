from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),

}

with DAG(
    dag_id="production_elt_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["elt", "snowflake", "dbt"],
    default_args=default_args,
) as dag:
    
    ingest_data = BashOperator(
        task_id="ingest_data",
        bash_command="""
        cd /opt/airflow/project &&
        python ingestion/ingest.py
        """,
    )

    source_freshness = BashOperator(
    task_id="source_freshness",
    bash_command="""
    cd /opt/airflow/project/productioneltplatform &&
    dbt source freshness
    """,
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="""
        cd /opt/airflow/project/productioneltplatform &&
        dbt run
        """,
    )

    test_dbt = BashOperator(
        task_id="test_dbt",
        bash_command="""
        cd /opt/airflow/project/productioneltplatform &&
        dbt test
        """,
    )

    ingest_data >> source_freshness >> run_dbt >> test_dbt
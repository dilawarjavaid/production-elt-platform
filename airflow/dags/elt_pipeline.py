from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="production_elt_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["elt", "snowflake", "dbt"],
) as dag:
    
    ingest_data = BashOperator(
        task_id="ingest_data",
        bash_command="""
        cd /opt/airflow/project &&
        python ingestion/ingest.py
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

    ingest_data >> run_dbt >> test_dbt
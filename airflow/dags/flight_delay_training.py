from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'flight_delay_training',
    default_args=default_args,
    description='Pipeline de entrenamiento del modelo de retraso de vuelos',
    schedule_interval='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    ingest = BashOperator(
        task_id='ingest_data',
        bash_command='docker exec practica_creativa-flask-1 python resources/ingest.py',
    )

    train = BashOperator(
        task_id='train_model',
        bash_command='docker exec practica_creativa-flask-1 python resources/train_spark_mllib_model.py .',
    )

    ingest >> train

import logging
import airflow
import os

from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.postgres_dict import PostgresDictOperatorXcom
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators import PythonOperator
from airflow.operators import DummyOperator

from dags.data_sprints_dag.utils import (
    download_file,
    check_is_json,
    transform_columns,
    insert_df_to_db,
    check_is_csv,
    check_schema_exists,
)

log = logging.getLogger("Clean Trip Files")

module_name = "-".join(Path(__file__).parts[3:]).replace(".py", "")

default_args = {
    "owner": "oracy_martos",
    "depends_on_past": True,
    "start_date": datetime(2020, 7, 30, 23, 00),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(module_name, default_args=default_args,
          schedule_interval=timedelta(hours=24),
          max_active_runs=1, concurrency=1)

source_path = "/source"
transform_path = "/transform"
insert_path = "/to_insert"

with dag:
    json_files = [
        'data-sample_data-nyctaxi-trips-2009-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2010-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2011-json_corrigido.json',
        'data-sample_data-nyctaxi-trips-2012-json_corrigido.json',
        ]

    csv_files = [
        'data-payment_lookup-csv.csv',
        'data-vendor_lookup-csv.csv',
    ]

    start = DummyOperator(task_id='start', dag=dag)
    json_dowload = DummyOperator(task_id='json_dowload', dag=dag)
    csv_dowload = DummyOperator(task_id='csv_dowload', dag=dag)
    transform_csv = DummyOperator(task_id='transform_csv', dag=dag)
    transform_json = DummyOperator(task_id='transform_json', dag=dag)
    create_columns = DummyOperator(task_id='create_columns', dag=dag)
    insert_to_db = DummyOperator(task_id='insert_to_db', dag=dag)

    files_tasks_json = []
    for file_to_download in json_files:
        file_task = PythonOperator(
            task_id=f"download_{file_to_download}",
            python_callable=download_file,
            provide_context=True,
            op_kwargs={
                "download_path": source_path,
                "file_name": f'{file_to_download}',
            }
        )
        files_tasks_json.append(file_task)

    files_tasks_csv = []
    for file_to_download in csv_files:
        file_task = PythonOperator(
            task_id=f"download_{file_to_download}",
            python_callable=download_file,
            provide_context=True,
            op_kwargs={
                "download_path": source_path,
                "file_name": f'{file_to_download}',
            }
        )
        files_tasks_csv.append(file_task)

    check_is_json_tasks = []
    for json_file in json_files:
        check_is_json_task = PythonOperator(
            task_id=f"is_json_{json_file}",
            python_callable=check_is_json,
            provide_context=True,
            op_kwargs={
                "source_path": source_path,
                "transform_path": transform_path,
                "file_name": f'{json_file}',
            },
        )
        check_is_json_tasks.append(check_is_json_task)

    check_is_csv_tasks = []
    for csv_file in csv_files:
        check_is_csv_task = PythonOperator(
            task_id=f"is_csv_{csv_file}",
            python_callable=check_is_csv,
            provide_context=True,
            op_kwargs={
                "source_path": source_path,
                "transform_path": insert_path,
                "file_name": f'{csv_file}',
            }
        )
        check_is_csv_tasks.append(check_is_csv_task)

    json_transform_columns = []
    for json_file in json_files:
        json_transform_column = PythonOperator(
            task_id=f"create_columns_{json_file}",
            python_callable=transform_columns,
            provide_context=True,
            op_kwargs={
                "source_path": transform_path,
                "file_name": f'{json_file}',
            },
        )
        json_transform_columns.append(json_transform_column)

    check_schema_exists = PythonOperator(
        task_id="check_schema_exists",
        python_callable=check_schema_exists,
    )

    json_insert_list = []
    all_files = []
    all_files.extend(json_files)
    all_files.extend(csv_files)
    for json_file in all_files:
        json_insert = PythonOperator(
            task_id=f"insert_{json_file}",
            python_callable=insert_df_to_db,
            provide_context=True,
            op_kwargs={
                "source_path": insert_path,
                "file_name": f'{json_file}',
            },
        )
        json_insert_list.append(json_insert)

    start >> json_dowload
    json_dowload >> files_tasks_json
    start >> csv_dowload
    csv_dowload >> files_tasks_csv
    for file_task_csv in files_tasks_csv:
        file_task_csv >> transform_csv
    for file_task_json in files_tasks_json:
        file_task_json >> transform_json
    transform_json >> check_is_json_tasks >> create_columns
    transform_csv >> check_is_csv_tasks >> insert_to_db
    create_columns >> json_transform_columns
    json_transform_columns >> insert_to_db
    insert_to_db >> check_schema_exists
    check_schema_exists >> json_insert_list

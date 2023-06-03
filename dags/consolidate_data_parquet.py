
import pendulum
from datetime import datetime
import pandas
from glob import glob
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.edgemodifier import Label
from airflow.utils.trigger_rule import TriggerRule

from dags import PATH_FILE_PROCESSING, PATH_FILE_SILVER
from plugins.operators.downloand_file import DownlondFileOperator
from plugins.operators.remove_file_bucket import RemoveFileBucketOperator
from helpers.function_generics_operator import generate_empty_operator, generate_bash_operator
from helpers.methods_geral import check_files_exists
from service.data_base import DataBaseService



dag = DAG(
    dag_id="consolidate_data_parquet",
    description="consolidate data parquet",
    start_date=datetime(2023, 6, 7),
    schedule_interval='*/40 * * * *'
)

def save_data() -> None:
    file_gold = glob('./temp/processing/*.parquet')
    data_frame = pandas.concat((pandas.read_parquet(file) for file in file_gold))
    data_frame_path = f"./temp/silver/{pendulum.now().timestamp()}.parquet"
    data_frame.to_parquet(path=data_frame_path)

    DataBaseService().save_data(data_frame_path=data_frame_path)

check_file_processing_operator = BranchPythonOperator(
    task_id='check_file_in_processing',
    op_kwargs={
        'bucket_name': 'processing',
        'task_id_success': 'downland_file_in_processing',
        'task_id_falled': 'finish_task'},
    python_callable=check_files_exists,
    dag=dag
)

downland_file_processing_operator = DownlondFileOperator(
    task_id='downland_file_in_processing',
    dag=dag,
    bucket_name="processing"
)


save_data_set = PythonOperator(
    task_id='save_data_set',
    python_callable=save_data,
    dag=dag
)


remove_files_bucket = RemoveFileBucketOperator(
    task_id='remove_file_from_local',
    bucket_name="processing",
    dag=dag
)
clean_task = generate_bash_operator(task_id="complete_task",
    bash_command=f"rm -f {PATH_FILE_SILVER}/*.parquet;rm -f {PATH_FILE_PROCESSING}/*.parquet",
    dag=dag)

finish_task = generate_empty_operator(dag=dag,task_id="finish_task", trigger_rule=TriggerRule.NONE_FAILED)

check_file_processing_operator >> [downland_file_processing_operator, finish_task]
downland_file_processing_operator >> save_data_set >> remove_files_bucket >> clean_task >> finish_task

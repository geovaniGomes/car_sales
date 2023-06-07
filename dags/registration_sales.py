import os
import camelot
from datetime import datetime
import pandas
from airflow import DAG
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

from dags import PATH_FILE_PROCESSING, PATH_FILE_LANDING
from plugins.operators.downloand_file import DownlondFileOperator
from plugins.operators.put_file_by_bucket import PutFileByBucketOperator
from plugins.operators.remove_file_bucket import RemoveFileBucketOperator
from helpers.function_generics_operator import generate_empty_operator, generate_bash_operator
from helpers.methods_geral import check_files_exists,  generate_reference_month


dag = DAG(
    dag_id="data_ingestion",
    description="ingestion data to processing",
    start_date=datetime(2023, 6, 7),
    schedule_interval='*/15 * * * *'
)


def extract_table_of_file_pdf():
    columns = [
        'automobiles_ranking',
        'automobiles_model',
        'automobiles_licensed',
        'commercial_ranking',
        'commercial_model',
        'commercial_licensed',
        'month_reference',
        'year_reference',
        'reference_information']

    files_list_names = []
    list_values_data_frame = []
    slice_start = 2 
    slice_end = 52
    values_data_frame_finaly = []

    PAGE_EXTRACT_TABLE_DEFAULT = 5

    for file_name in os.listdir(PATH_FILE_LANDING):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(PATH_FILE_LANDING, file_name)
            data_frame = camelot.read_pdf(
                file_path,
                flavor='stream',
                flag_size=True,
                pages=str(PAGE_EXTRACT_TABLE_DEFAULT+1))[0].df
            list_values_data_frame.extend(data_frame.values.tolist())
            files_list_names.append(file_name[:7])
        else:
            continue
    

    for file_name in files_list_names:
        year, month = file_name.split('_')
        month_format = generate_reference_month(month)
    
        list_values =  list_values_data_frame[slice_start:slice_end].copy()
        for item in list_values:
            item.append(month_format)
            item.append(year)
            item.append(file_name)
                    
            values_data_frame_finaly.append(item)

        slice_start = (2 + slice_end)
        slice_end = (slice_end + 52)

    df = pandas.DataFrame(values_data_frame_finaly, columns=columns)

    df.to_parquet(
        path=f"{PATH_FILE_PROCESSING}/{str(datetime.now().timestamp())}.parquet",
        index=False)


check_file_operator = BranchPythonOperator(
    task_id='check_file_in_data_lake',
    op_kwargs={
        'bucket_name': 'landing',
        'task_id_success': 'downland_file_in_data_lake',
        'task_id_falled': 'finish_task'},
    python_callable=check_files_exists,
    dag=dag
)

downland_file_operator = DownlondFileOperator(
    task_id='downland_file_in_data_lake',
    dag=dag
)

extract_table_pdf_to_parquet = PythonOperator(
    task_id='extract_table_pdf_to_parquet',
    python_callable=extract_table_of_file_pdf,
    dag=dag
)


push_file_to_data_lake = PutFileByBucketOperator(
    task_id='push_file_to_data_lake',
    dag=dag,
    bucket_name="processing",
    path_local=PATH_FILE_PROCESSING
)

remove_files_bucket = RemoveFileBucketOperator(
    task_id='remove_file_from_local',
    bucket_name="landing",
    dag=dag
)

clean_task = generate_bash_operator(task_id="complete_task",
    bash_command=f"rm -f {PATH_FILE_LANDING}/*.pdf;rm -f {PATH_FILE_PROCESSING}/*.parquet",
    dag=dag)


finish_task = generate_empty_operator(dag=dag,task_id="finish_task", trigger_rule=TriggerRule.NONE_FAILED)

check_file_operator >> [downland_file_operator, finish_task]
downland_file_operator >> extract_table_pdf_to_parquet >> push_file_to_data_lake >> remove_files_bucket >> clean_task >> finish_task

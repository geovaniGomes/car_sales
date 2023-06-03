from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from enum import Enum
from airflow import DAG

def generate_empty_operator(dag: DAG, task_id:str, trigger_rule:Enum) -> EmptyOperator:
    return EmptyOperator(dag=dag, task_id=task_id, trigger_rule=trigger_rule)

def generate_bash_operator(dag: DAG, task_id: str, bash_command:str) -> BashOperator:
    return BashOperator(task_id=task_id, bash_command=bash_command, dag=dag)

FROM python:3.9.13 as builder

RUN mkdir /airflow

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AIRFLOW_HOME=/airflow
ENV AIRFLOW__CORE__DAGS_FOLDER=$AIRFLOW_HOME/dags
ENV PLUGINS_FOLDER=$AIRFLOW_HOME/plugins
ENV LOGS_FOLDER=$AIRFLOW_HOME/logs
ENV CHILD_PROCESS_LOG_DIRECTORY=$AIRFLOW_HOME/logs/scheduler/
ENV DAG_PROCESSOR_MANAGER_LOG_LOCATION=$AIRFLOW_HOME/logs/dag_processor_manager/dag_processor_manager.log
ENV AIRFLOW__CORE__FERNET_KEY="e_ebmnhdDT_JQSEh04gSVXW7VuzhFQOPuerC7yvYJYw="
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV WEBSERVER_MONITOR_PID_LOCATION=$AIRFLOW_HOME/logs
# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y build-essential libffi-dev python-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod -R 777 airflow/
# Cópia dos arquivos do projeto

COPY dags/ /airflow/dags/
COPY plugins/ /airflow/plugins/
COPY ./webserver_config.py /airflow/webserver_config.py
COPY ./start_airflow.sh /airflow/start_airflow.sh
RUN chmod +x /airflow/start_airflow.sh

# Exposição da porta do Webserver
EXPOSE 5000

# Inicialização do Airflow
ENTRYPOINT ["/airflow/start_airflow.sh"]

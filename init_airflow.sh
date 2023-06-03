#!/bin/bash
source models.models.py


airflow db init

airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com


python -c 'from models.models import db; db.create_all()'

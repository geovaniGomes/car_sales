#!/bin/bash
set -e


airflow webserver -p 5000 -D &
airflow scheduler -D
import os
import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from service.minio import DataLakeService


class PutFileByBucketOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        bucket_name:str,
        path_local:str,
        *args, **kwargs,
        ) -> None:

        super(PutFileByBucketOperator, self).__init__(*args, **kwargs)
        self.data_lake = DataLakeService(bucket_name=bucket_name)
        self.path_local = path_local
        
    def execute(self, context):
        files = []
        for file_name in os.listdir(self.path_local):
            if file_name.endswith('.parquet'):
                file_path = os.path.join(self.path_local, file_name)
                files.append(file_path)
            else:
                continue
        logging.info(files)
        for file in files:
            self.data_lake.upload_file(file_path=file)
        
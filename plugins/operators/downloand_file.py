import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from service.minio import DataLakeService

class DownlondFileOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        bucket_name:str = "landing",
        *args, **kwargs) -> None:

        super(DownlondFileOperator, self).__init__(*args, **kwargs)
        self.data_lake = DataLakeService(bucket_name)

        
    def execute(self, context):
        objects = list(self.data_lake.list_objects())
        list_files = []
        if len(objects) > 0:
            self.log.info("new files avalable!")
            try:
                for file in objects:
                    object_name = file.object_name
                    list_files.append(object_name)
                    self.log.info(f"downloand file: {object_name}")
                    self.data_lake.downland_file(object_name=object_name)
                    context['ti'].xcom_push(key="remove_files", value=list_files)
            except Exception as e:
                self.log.info(f"Error getting file: {object_name}")
                self.log.error(e)
        
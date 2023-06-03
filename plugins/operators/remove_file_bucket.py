from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from service.minio import DataLakeService


class RemoveFileBucketOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        bucket_name:str,
        *args, **kwargs) -> None:

        super(RemoveFileBucketOperator, self).__init__(*args, **kwargs)
        self.data_lake = DataLakeService(bucket_name=bucket_name)
        self.bucket_name = bucket_name
        
    def execute(self, context) -> None:
        list_file_name_to_remove = list(context['ti'].xcom_pull(key="remove_files"))
        context['ti'].xcom_push(key="remove_files", value=[])

        for file in list_file_name_to_remove:
            self.log.info(f"remove file: {file}")
            self.data_lake.remove_object(object_name=file)

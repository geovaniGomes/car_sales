import os
import logging
from minio import Minio


class DataLakeService(object):

    def __init__(self, bucket_name:str = "landing") -> None:
        self.__minio_client = Minio(
            endpoint=os.environ.get('MINIO_DATA_LAKE_URL'),
            access_key=os.environ.get('MINIO_ROOT_USER'),
            secret_key=os.environ.get('MINIO_ROOT_PASSWORD'),
            secure=False  # SSL habilitado
        )
        self.bucket_name = bucket_name
        self.__validate_bucket_exists(self.bucket_name)
        self.__SAVE_FILE_PATH = f"{os.path.dirname(os.path.abspath(__file__)).split('service')[0]}temp/{self.bucket_name}"

    def list_objects(self) -> list:
        self.__validate_bucket_exists(self.bucket_name)
        return self.__minio_client.list_objects(bucket_name=self.bucket_name)

    def create_bucket(self) -> bool:
        try:
            self.__minio_client.make_bucket(self.bucket_name)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def upload_file(self, file_path: str) -> None:
        self.__validate_bucket_exists(bucket_name=self.bucket_name)
        try:
            self.__minio_client.fput_object(
                bucket_name=self.bucket_name,
                object_name=file_path.split('/')[-1],
                file_path=file_path)

        except Exception as e:
            logging.error(e)
            raise Exception('Unable to upload the file.')

    def downland_file(self, object_name: str) -> None:

        try:
            self.__minio_client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=f"{self.__SAVE_FILE_PATH}/{object_name}")
        except Exception as e:
            logging.error(e)
            raise Exception('Unable to downloand the file.')

    def remove_object(self, object_name: str) -> None:
        try:
            self.__validate_bucket_exists(bucket_name=self.bucket_name)
            self.__minio_client.remove_object(bucket_name=self.bucket_name, object_name=object_name)
        except Exception as e:
            logging.error(e)
            raise Exception('Unable to remove the file.')
    
    def __validate_bucket_exists(self, bucket_name: str) -> None:
        if not self.__minio_client.bucket_exists(bucket_name):
            raise Exception(f'Bucket {bucket_name} not exists.')

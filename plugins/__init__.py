from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin
from plugins.operators.downloand_file import DownlondFileOperator
from plugins.operators.put_file_by_bucket import PutFileByBucketOperator
from plugins.operators.remove_file_bucket import RemoveFileBucketOperator



class MyPlugins(AirflowPlugin):
    name = "my_plugin"
    operators = [DownlondFileOperator, PutFileByBucketOperator, RemoveFileBucketOperator]

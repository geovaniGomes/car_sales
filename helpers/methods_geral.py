from service.minio import DataLakeService


def check_files_exists(bucket_name: str, task_id_success: str, task_id_falled: str) -> str:
    return task_id_success if list(DataLakeService(bucket_name=bucket_name).list_objects()) else task_id_falled

def generate_reference_month(month:str) -> str:
    month_dict = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro"
    }
    return month_dict[month]

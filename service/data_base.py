import os
import psycopg2
import logging
import pandas
from glob import glob
from sqlalchemy.orm import sessionmaker
from models.models import db, RakingSalesCar



class DataBaseService(object):
    
    def __init__(self) -> None:
        self._Session = sessionmaker(bind=db.get_engine())
        self._session = self._Session()


    def save_data(self, data_frame_path: str) -> None:       
        file_gold = glob('./temp/silver/*.parquet')
        data_frame = pandas.concat((pandas.read_parquet(file) for file in file_gold))

        reference_information_counts = data_frame['reference_information'].value_counts()
        reference_information_list = list(reference_information_counts.index)

        raking_sales = RakingSalesCar.query.all()

        if not raking_sales:
            insert_values = reference_information_list
        else:

            insert_values = [reference_information for raking in raking_sales
                                for reference_information in reference_information_list
                                if not raking.reference_information == reference_information]
        
            insert_values = list(set(insert_values))
        
        data_frame_to_insert  = data_frame.query("reference_information==@insert_values")

        data_frame_to_insert['automobiles_licensed'] = data_frame_to_insert['automobiles_licensed'].apply(self.remove_character_special)
        data_frame_to_insert['commercial_licensed'] = data_frame_to_insert['commercial_licensed'].apply(self.remove_character_special)

        data_frame_to_insert['automobiles_licensed'] = data_frame_to_insert['automobiles_licensed'].astype(int)
        data_frame_to_insert['commercial_licensed'] =  data_frame_to_insert['commercial_licensed'].astype(int)

        list_raking_sales_car = []
        for index, column in data_frame_to_insert.iterrows():
            list_raking_sales_car.append(
                RakingSalesCar(
                    automobiles_ranking=column['automobiles_ranking'],
                    automobiles_model=column['automobiles_model'],
                    automobiles_licensed=column['automobiles_licensed'],
                    commercial_ranking=column['commercial_ranking'],
                    commercial_model=column['commercial_model'],
                    commercial_licensed=column['commercial_licensed'],
                    month_reference=column['month_reference'],
                    year_reference=column['year_reference'],
                    reference_information=column['reference_information']                   
            ))
        
        try:
            self._session.bulk_save_objects(list_raking_sales_car)
            self._session.commit()
        except Exception as e:
            logging.error(e)
            self._session.rollback()
            raise Exception('Unable to save records.')
        finally:
            self._session.close()
    
    def remove_character_special(self, data) :
        return data.replace('.', '')
        
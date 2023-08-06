# REMOVE THIS FILE ON NOVEMBER 2022 POST RELEASE OF ACTUAL DEEPGOTDATA

from typing import Union 

class GotDataPull():

    def __init__(self, dataset_id, data_path: Union[None, str]):
        self.dataset_id = dataset_id
        self.data_path = data_path
    
    def pull_data_by_id(self):
        print(f"Pulling the dataset under {self.dataset_id} from DeepGotData database.")

    def __check_data_type__(self):
        pass
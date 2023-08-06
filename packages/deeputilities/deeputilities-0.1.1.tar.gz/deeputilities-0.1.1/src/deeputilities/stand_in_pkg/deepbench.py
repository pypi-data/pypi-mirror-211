# REMOVE THIS FILE ON NOVEMBER 2022 POST RELEASE OF ACTUAL DEEPBENCH
from typing import Union 

class Catalogue():

    def __init__(self, n_obj: int, pix_dim: int, data_type: str, image_type: str, data_path: Union[None, str]):
        self.n_obj = n_obj
        self.pix_dim = pix_dim
        self.data_type = data_type
        self.image_type = image_type
    
    def get_catalogue(self):
        pass
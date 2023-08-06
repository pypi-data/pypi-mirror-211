from typing import List

class Ingest():

    def __init__(self, data_input: str, data_path:str= None, label_path:str= None, transforms: List[str]=None):
        
        self.data_input = data_input
        self.data_path = data_path
        self.target_path = label_path
        self.transforms = transforms
    
    # Read in the raw data to a dataframe or array.
    def parse_raw_data(self):
        pass

    # Convert image files into arrays and append. One-hot-encode annotations if they are categorical.
    def parse_images_with_annotations(self):
        pass

    def parse_image_folders(self):
        pass

    def parse_csv(self):
        pass

    def parse_array(self):
        pass

    def parse_h5(self):
        pass

    def __get_labels_from_folders__(self):
        pass 

    def __check_file_path_exists__(self):
        pass

    # Add data to a Dataset class.

    # Read in raw image with annotation file combination.

    # Read in a csv to dataframe.

    # Read in raw by folder.

    # Read in raw array pair.

    # Read raw by h5 file.

    # Read in raw from DeepBench.

    # Ingest from GotData.

    # Ingest from example datasets.

    # Add data to image dataset class.

    # Add to h5 dataset class.

    # Add to numpy dataset class.
    
    # Get label names from folders.

    # Check if a file path is valid.

    # Check what the data type is in the data folder.
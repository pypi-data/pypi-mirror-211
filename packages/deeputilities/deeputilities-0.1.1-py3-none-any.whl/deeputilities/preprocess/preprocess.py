import pandas as pd 
import numpy as np
from settings import OUTPUT_PATH

class Preprocess():
    """ Includes EDA, data pre-processing, and cleaning."""

    def __init__(self, raw_data: pd.DataFrame | np.array, data_logging_path: str="data_logging.json", clean_data_path:str=f"{OUTPUT_PATH}/clean_data"):

        self.data = raw_data
    
    # Run all of the preprocessing steps.

    # Using pandas profiling, do EDA.

    # Implement data augmentation

    # Function to replace the missing data.

    # Function to strip whitespace from data.

    # Function to replace missing values with NaN.

    # Remove samples with more than one missing field.

    # Run data interpolation for the dataframe.

    # Remove all missing values.

    # Remove any outliers.

    # Perform one-hot-encoding for a specific label.

    # Write out the preprocessing steps taken as a logging dictionary. Put variables in settings.



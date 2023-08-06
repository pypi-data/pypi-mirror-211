from src.deeputilities.settings import CONFIG_DICT_DEFAULT
from src.deeputilities.configuration.yaml_functions import YAMLOperator
from typing import List

class ConfigObject():

    def __init__(self, config_file_path: str=None):

        if config_file_path is not None:
            self.yaml_ops = YAMLOperator(file_path=config_file_path)
            config_dict = self.yaml_ops.parse_yaml()

            self.__check_valid_config__(config_dict)

            self.config_dict = config_dict
        else:
            self.config_dict = None

    # Property that returns the dictionary
    @property
    def config_dict(self):

        return self.config_dict

    # Property that returns data.
    @property
    def data(self):

        return self.config_dict["DATA"]

    # Property that returns model data.
    @ property
    def model_data(self):

        return self.config_dict["MODEL_DATA"]

    # Property that returns model params.
    @property
    def model_parameters(self):

        return self.config_dict["MODEL_PARAMS"]

    # Property that returns output.
    @property
    def output(self):

        return self.config_dict["OUTPUT"]
    
    def create_default_configs(self, config_types: List[str]):
    
        for template_type in config_types:
            if template_type == "ALL":
                # Run all of the yaml creation functions.
                break
            elif template_type == "BENCH":
                # Call the DeepBench method. Make the filename default the same as the utils one.
                pass
            elif template_type == "DEEPGOTDATA":
                # Call the DeepGotData method. Make the filename default the same as the utils one.
                pass
            elif template_type == "UTILS":
                self.yaml_ops.create_initial_yaml()
            else:
                raise ValueError("An invalid configuration template type has been input. \
                                Only ALL, UTILS, BENCH, and GOTDATA are valid values.")

    
    def __check_valid_config__(self, config_dict):

        self.__check_valid_config_params__(config_dict=config_dict)
        self.__check_valid_config_values__(config_dict=config_dict)
        self.__check_valid_config_paths__(config_dict=config_dict)
    
    def __check_valid_config_params__(self, config_dict):

        config_key_list = self.yaml_ops.get_yaml_options(yaml_dict=config_dict)
        correct_key_list = self.yaml_ops.get_yaml_options(yaml_dict=CONFIG_DICT_DEFAULT)

        if not set(config_key_list) == set(correct_key_list):
            for key in config_key_list:
                if not key in correct_key_list:
                    raise KeyError(f"{key} is not a valid parameter for a configuration file. \
                                   Valid parameters are: {correct_key_list}. Please change the invalid parameter or \
                                   create a default yaml using the appropriate function.")
    
    # TODO: Fill method for config value check.
    def __check_valid_config_values__(self, config_dict):
        
        # Check that the data configuration style given is valid.

        # Check that the base model given is valid, if filled.

        # Check that the optimizer matches the available values.
        pass
    
    # TODO: Fill method for config path check.
    def __check_valid_config_paths__(self, config_dict):

        # Check that if using LABELLED_W_ANNOTATIONS or NUMPY that data and label paths are given.

        # Check that if using LABELLED_W_FOLDERS or UNLABELLED or H5 data path is given.

        # Check that the user model path is valid if USER_MODEL is filled.
        pass



                


import yaml
from typing import Union
import os
from src.deeputilities.settings import CONFIG_DICT_DEFAULT
from datetime import datetime
from src.deeputilities.settings import CONFIG_PATH

# TODO: Add a check for file path validity.
class YAMLOperator():

    def __init__(self, file_path: Union[None, str]):

        self.file_path = file_path 

    def parse_yaml(self):
        """
        Parse a YAML file and return a dictionary.

        Args:
            file_path (str): Path to the YAML file.

        Returns:
            dict: Dictionary containing the parsed YAML file.
        
        Raises:
            yaml.YAMLError: If the YAML file is not valid.
        """
        with open(self.file_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def update_yaml(self, variables: dict):
        """
        Update a YAML file with the variables provided.

        Args:
            variables (Dict): Dictionary of variables to change and their updated values.
            file_path (str): Path to the YAML file.

        Returns:
            None
        
        Raises:
            yaml.YAMLError: If the YAML file is not valid.
            ValueError: If the variable is not in the YAML file.
        """
        yaml_dict = self.parse_yaml()
        yaml_options = self.get_yaml_options(yaml_dict=yaml_dict)

        for variable in variables:
            if variable.lower().strip() not in yaml_options:
                raise ValueError(f"Variable {variable} is not an option in the YAML file. The options are as follows: {yaml_options}")
            
        original_config = self.parse_yaml(self.file_path)

        for section in original_config.keys():
            for key in original_config[section].keys():
                if key in variables:
                    original_config[section][key] = variables[key]

        with open(self.file_path, 'w') as yaml_file:
            yaml_file.write( yaml.dump(original_config, default_flow_style=False))

    def get_yaml_options(self, yaml_dict: dict):

        yaml_key_list = []

        for k in yaml_dict.keys():
            yaml_key_list.append(k.lower().strip())
            for k_2 in yaml_dict[k].keys():
                yaml_key_list.append(k_2.lower().strip())

        return yaml_key_list

    def create_initial_yaml(self, variables: dict=CONFIG_DICT_DEFAULT, filename=f"{CONFIG_PATH}/deeputils_config_{datetime.now}.yaml"):
        
        if not os.path.exists((self.file_path + filename)):
            with open(self.file_path, 'w') as yaml_file:
                yaml_file.write(yaml.dump(variables, default_flow_style=False))
        else:
            raise ValueError(f"The file {self.file_path} already exists. If you'd like to use another config file, you need to change the file name.")
                
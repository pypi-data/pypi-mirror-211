from cleo.commands.command import Command
from src.deeputilities.client.options.options import bench_config_path, gotdata_config_path, preprocess_data, config_file_path
from cleo.helpers import argument
from src.deeputilities.settings import CONFIG_DICT_DEFAULT
from src.deeputilities.configuration.configuration_object import ConfigObject
from src.deeputilities.ingest.ingestion import Ingest
from src.deeputilities.settings import USER_DATA_CONFIGS
from src.deeputilities.settings import EXAMPLE_DATA_CONFIGS
import os
import time


class IngestCommand(Command):

    name = 'ingest'
    description = 'Ingest the user\'s data and provide a torch Dataset.'
    arguments = [
        config_file_path,
        bench_config_path,
        gotdata_config_path,
        preprocess_data
    ]
    help = ''

    def handle(self):
        self.write("Welcome to DeepUtilities!")

        config_file_path = self.argument("config-file-path")
        bench_config = self.argument("bench_config_path")
        got_config = self.argument("gotdata_config_path")

        if not config_file_path:
            raise FileNotFoundError("The path {config_file_path} is invalid. \
                                    You'll have to use a configuration yaml to run DeepUtilities. \
                                    Run the --help command to figure how to produce a default file, if need be.")
        else:
            config = ConfigObject(config_file_path)

        self.write("Configuration file has been successfully parsed.")

        time.sleep(2.0)

        self.overwrite("Your data is being ingested.")

        data_input = config.data["INPUT"]

        # TODO: Replace container clause with method for producing Bench config file from utils.
        if data_input == "DEEPBENCH": 
            if (bench_config is None or not os.path.exists(bench_config)):
                raise FileNotFoundError("If you're generating data from DeepBench, \
                                        you must provide a configuration file for DeepBench. \
                                        Run <INSERT-METHOD-FOR-RUNNING-BENCH-FROM-UTILS.>")
            else:
                config.data["DATA PATH"] = bench_config
                # TODO: Produce the data. 

        # TODO: Replace container clause with method for producing DGD config file.
        if data_input == "GOTDATA":
            if (got_config is None or not os.path.exists(got_config)):
                raise FileNotFoundError("If you're generating data from DeepGotData, \
                                        you must provide a configuration file for DeepGotData. \
                                        Run <INSERT-METHOD-FOR-RUNNING-GOTDATA-FROM-UTILS.>")
            else:
                config.data["DATA_PATH"] = got_config
                # TODO: Produce the data.            

        ingestor = Ingest(data_input=data_input, data_path=config.data["DATA_PATH"], label_path=config.data["LABEL_PATH"], transforms=config.data["TRANSFORMS"])

        # Read in the raw data.
        
        # If preprocess argument was provided, run preprocessing.

        # Check which preprocess options/methods have been provided and run them accordingly. 

        # Read the now preprocessed data into the correct Dataset.

        self.overwrite(f"Your {data_input} data has been ingested!")

        




from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option
from src.deeputilities.settings import CONFIG_DICT_DEFAULT
from configuration.yaml_functions import YAMLOperator


class DeepUtilsFullRunCommand(Command):

    name = 'full-run'
    description = 'Go through a full run of the deep utilities workflow.'
    arguments = [
        argument(
            "config-file-path",
            "The path to a yaml file including all of the configuration needed to perform the analysis.",
            optional=False,
            multiple=False,
        )

    ]
    options = [
        option(long_name='data_path', short_name='d', description=('Path to the data file.')),
        option(long_name='label_path', short_name='l', description='Path to the label file.'),
        option(long_name='model', short_name='m', description='Model to use.'),
        option(long_name='task_type', short_name='t', description='Task type.'),
        option(long_name='batch_size', short_name='b', description='Batch size.'),
        option(long_name='learning_rate', short_name='r', description='Learning rate.'),
        option(long_name='optimizer', short_name='o', description='Optimizer.'),
        option(long_name='output_path', short_name='p', description='Output path.'),
        option(long_name='data_configuration', short_name='c', description='Data configuration.')
        ]
    help = ''

    def handle(self):

    # 0. Parse or create the configuration file for the application.
        self.write("Welcome to DeepUtilities!")
        config_bool = input("Let's set up your project by starting with your configuration file. If you do not have one, one will initialized at the path provided. Do you already have a configuration file?")
        if not config_bool:
            config_dict_bool= input("Please provide the dictionary for your configuration file. If not provided, values will be set for you.")
            if not config_dict_bool:
                config_dict_init = CONFIG_DICT_DEFAULT
            else:
                data_path = self.option('data_path')
                label_path = self.option('label_path')
                model = self.option('model')
                task_type = self.option('task_type')
                batch_size = self.option('batch_size')
                learning_rate = self.option('learning_rate')
                optimizer = self.option('optimizer')
                output_path = self.option('output_path')
                configuration = self.option('data_configuration')
                config_dict_init = {
                    "DATA": {
                        "CONFIGURATION": configuration,
                        "DATA_PATH": data_path,
                        "LABEL_PATH": label_path
                    },
                    "MODEL_DATA": {
                        "MODEL": model,
                        "TASK_TYPE": task_type,
                    },
                    "MODEL_PARAMS": {
                        "BATCH_SIZE": batch_size,
                        "LEARNING_RATE": learning_rate,
                        "OPTIMIZER": optimizer,
                    },
                    "OUTPUT": {
                        "OUTPUT_PATH": output_path
                    }
                }
    
        self.write("Running Config Creation/Parsing...")
        config_file_path= self.argument("config-file-path")
        yaml_op = YAMLOperator(file_path=config_file_path)

        if not config_bool:
            yaml_op.create_initial_yaml(variables=config_dict_init)
        else:
            config_dict = yaml_op.parse_yaml()

    # 2. Run the EDA pipeline.
        self.overwrite("Running Data Ingestion...") 
        self.call("ingest", arguments=[config_dict, config_file_path])

    # 3. Run the pre-process module.
        self.overwrite("Running Data Pre-Processing and Analysis...")
        self.call("preprocess", arguments=[config_dict])

    # 4. Train/Test/.
        self.overwrite("Running Model Training, Testing, Architecture Search...")
        self.call("model", arguments=[config_dict])

    #5. Architecture search
        self.overwrite("Running Diagnostic Output...")
        self.call("diagnostic", arguments=[config_dict])


from cleo.commands.command import Command
from cleo.helpers import argument
from cleo.helpers import option
from settings import CONFIG_DICT_DEFAULT
from configuration.yaml_functions import YAMLOperator
from model.model import Model
from diagnosis.diagnostics import Diagnosis

import os
import numpy as np 

class DiagnosisCommand(Command):

    name = 'diagonsis'
    description = 'Run a model training, or run a lazy archeture search'
    arguments = [

        argument("config-dict", 
                 "Configurations to run the model training", 
                 optional=False, 
                 multiple=False), 
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
                data_path = self.option('data_path')
                label_path = self.option('label_path')
                model = self.option('model')
                task_type = self.option('task_type')
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

        self.overwrite("Running Data Ingestion...") 
        #TODO Get the output of the ingestion set
        _, test_loader = self.call("ingest", arguments=[config_dict, config_file_path])

    # 4. Test/Diagonsis

        self.overwrite("Testing stored model...")

        trained_model_path = f'{config_dict["OUTPUT"]["OUTPUT_PATH"]}/trained_model.json'
        train_prediction_path = f'{config_dict["OUTPUT"]["OUTPUT_PATH"]}/train_predictions.np'

        if (~os.path.exists(train_prediction_path) & ~os.path.exists(trained_model_path)):
            raise ValueError("Predictions and trained model not found at OUTPATH; please assure these files are present")
        
        train_predictions = np.load(train_prediction_path)

        loaded_model = Diagnosis.load_plot_model(trained_model_path)
        # TODO check the model module for a prediction method. There should be a way to do this. 
        test_predictions = loaded_model.predict(test_loader['images'])

        # TODO check for labelled vs unlabelled. 
            # Raise notimpl forunlabeled

        # TODO save the scores?????? Why are the scores not saved by the model module?????

        Diagnosis.true_pred(y_test=test_loader['labels'], y_pred=test_predictions)
        Diagnosis.loss_acc_plot(loss=loaded_model['loss'], val_loss=loaded_model["val_loss"], acc=["Accuary"], val_acc=['val_Accuarcy'] )
        Diagnosis.conf_matrix(y_test=test_loader['labels'], y_pred=test_predictions)
        









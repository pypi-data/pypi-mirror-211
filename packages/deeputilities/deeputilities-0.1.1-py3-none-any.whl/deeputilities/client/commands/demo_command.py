from cleo.commands.command import Command
from cleo.helpers import argument
from src.deeputilities.configuration.configuration_object import ConfigObject
from src.deeputilities.settings import CONFIG_PATH, CONFIG_DICT_DEFAULT
from src.deeputilities.client.options.options import bench_config_path
from src.deeputilities.client.options.options import gotdata_config_path
from src.deeputilities.client.options.options import preprocess_data
from src.deeputilities.client.options.options import config_file_path
from src.deeputilities.settings import OUTPUT_PATH
from src.deeputilities.client.options.options import config_type
import time
import pandas as pd
from ydata_profiling import ProfileReport
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier
from joblib import dump 
import os
import yaml



class DemoCommand(Command):

    name = 'demo'
    description = 'A user-demo meant to be used as an example of how to use DeepUtilies.'
    arguments = []
    options=[]
    help = ''

    def handle(self):
        self.write("Welcome to DeepUtilities built-in Demo!")
        
        self.write("We'll look at each of the major components of the library.\
                   Please don't use this as a replacement for the README directions,\
                   but rather as a supplement.")
        
        time.sleep(7)
        
        self.overwrite("Firstly, DeepUtilities requires the use of a configuration yaml. \
                   If you don't have one, you can run the following command: \
                   'deeputils make-config UTILS'. We'll run this command \
                   and make a utilities template!\n--------\ndeeputils make-config UTILS")
        
        time.sleep(7)
        
        # Make the configuration template.
        # self.call(name="make-config", arguments="UTILS")
        os.makedirs(CONFIG_PATH)

        with open(os.path.join(CONFIG_PATH, "utils_config.yaml") , 'w') as yaml_file:
            yaml_file.write(yaml.dump(CONFIG_DICT_DEFAULT, default_flow_style=False))


        self.overwrite("Check that your config file is in the path: \
                   your-current-directory/deeputilities/config_files/...")
        
        time.sleep(7)
        # Ingest command w/ preprocess options -
        # Ingest the titanic example data. Data should be saved to the default path.
        self.overwrite("Next, let's ingest some example data using the ingestion command.\
                        We'll download and ingest the Titanic example dataset.")
        
        data = pd.read_csv(filepath_or_buffer="https://www.kaggle.com/competitions/titanic/data?select=train.csv", on_bad_lines="skip")
        data.to_csv(f"{OUTPUT_PATH}/data/init_titanic_data.csv")
        
        time.sleep(7)

        self.overwrite(f"Now that the data has been downloaded, we run the ingestion command, \
                       along with data processing. We'll use the 'full processing' option \
                       that runs all relevant data processing steps, \
                       but you can also use individual modes of data cleaning. \
                       Check the documenation for more.:\
                       \n--------\ndeeputils ingest {CONFIG_PATH} --full-process")
        
        # Make sure the cleaned data gets saved to the correct default path.
        profile = ProfileReport(data, title="Titanic Profiling Report")
        profile.to_file(f"{OUTPUT_PATH}/data/titanic_report.html")

        data_no_nan = data.dropna(subset=["Fare"]).query('Fare != 0')

        # Make sure you removed all missing Fare rows.
        train_data = pd.get_dummies(data_no_nan, columns=['Sex'])

        # Take only the relevant columns.
        train_data = train_data.loc[:, ['Pclass', 'Survived', 'Fare', 'Sex_female', 'Sex_male']]
        y_train_data = train_data.loc[:, 'Survived']
        y_train_data.to_csv(f"{OUTPUT_PATH}/data/titanic_clean_labels.csv")

        # Finally remove Survived column from training data.
        x_train_data = train_data.drop('Survived', axis=1) 
        x_train_data.to_csv(f"{OUTPUT_PATH}/data/titanic_clean_data.csv")

        self.overwrite(f"Now that the data has been cleaned and ingested, \
                       we can find a model that performs the best for our problem.\
                       The ingestion command assumed labels were the first column of your csv.\
                       \n--------\ndeeputils model {CONFIG_PATH}")
        
        time.sleep(7)
        # Model command
        # Run the LazyPredict with the task set to classification. Extract the best
        # performing model and go forward with training.
        x_train, x_val, y_train, y_val = train_test_split(x_train_data, y_train_data, test_size=0.33, random_state=42)
        clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
        models,predictions = clf.fit(x_train, x_val, y_train, y_val)

        best_model = models['Accuracy'].idxmax()

        models = clf.provide_models(x_train, x_val, y_train, y_val)
        best_model = models[best_model]

        dump(best_model, f"{OUTPUT_PATH}/models/BaggingClassifier.joblib")

        # Evaluate command
        # Run diagnostics on the model performance. Find the acc, ROC/AUC, confusion.

        # Diagnosis command.
        self.overwrite(f"We found that our best model was a BaggingClassifier. Now we can evaluate its performance\
                       using diagnostic plots of our choosing. Let's say I want to see the training accuracy. We would run the following command:\
                       \n--------\ndeeputils diagnose {CONFIG_PATH} --train-accuracy")
        
        time.sleep(7)
        
        # Load saved model from the last run and 
        # run inference to see if you would survive the Titanic.
        self.overwrite(f"Saved user models can also be used for training and evaluation. \
                       For instance, let's load our saved model and see if we would survive the Titanic.\
                       \n--------\ndeeputils evaluate {OUTPUT_PATH}/models/BaggingClassifier.joblib --labels Sex: F Age: 22 Fare: 0")
        
        time.sleep(7)
        print("1")







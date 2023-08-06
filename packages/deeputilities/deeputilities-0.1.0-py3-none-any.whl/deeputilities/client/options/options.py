from cleo.helpers import option
from cleo.helpers import argument

# Arguments.

config_type = argument(
    name="config-type",
    description="The type of configuration the user needs produced. Can be 'ALL', 'UTILS', 'GOTDATA', or 'BENCH'.",
    optional=False,
    multiple=True,
)

config_file_path = argument(
            name="config-file-path",
            description=("The path to a yaml file including all of the configuration needed to perform the analysis."),
            optional=False,
            multiple=False,
        ),

bench_config_path = argument(
        name = 'bench-config-path', 
        description=("The configuration file for ingesting data using DeepBench."),
        optional=True,
)

gotdata_config_path = argument(
        name = "gotdata-config-path",
        description="The path to the configuration file for ingesting data using DeepGotData.",
        optional=True,
)

preprocess_data = argument(
    name = "preprocess-data",
    description="Flag that determines whether you want to preprocess the data being ingested.",
    optional=True,
)

# Options.

# Preprocess Options.
full_preprocess = option(
    long_name= "full-processing",
    description="Runs the full processing step, from data exploration profiles to data cleaning.",
    flag=True,
    value_required=False
)

eda = option(
    long_name="profile-data",
    description="Outputs the initial data profile using pandas-profiling output.",
    value_required=True,
    multiple=False
)
# data_augmentation = option()
# remove_missing_data = option()
# replace_missing_data = option()
# data_interpolation = option()
# remove_outliers = option()
# one_hot_encoding = option()

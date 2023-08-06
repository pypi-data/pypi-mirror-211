from cleo.commands.command import Command
from cleo.helpers import argument
from src.deeputilities.settings import CONFIG_DICT_DEFAULT
from src.deeputilities.client.options.options import config_type
from src.deeputilities.settings import CONFIG_TEMPLATE_TYPES
from src.deeputilities.configuration.configuration_object import ConfigObject
from src.deeputilities.settings import CONFIG_PATH

class ConfigMaker(Command):

    name = 'make-config'
    description = 'Creates default configuration files that can be used to use DeepUtilities, DeepBench, or DeepGotData.'
    arguments = []
    options = [
        config_type
    ]
         
    help = ''

    def handle(self):
        self.write("Welcome to DeepUtilities!")

        config_types = self.option("config-type")

        if not config_types or config_types not in CONFIG_TEMPLATE_TYPES:
            raise ValueError(f"You haven't provided a valid configuration template type(s). \
                             Valid values are as follows: {CONFIG_TEMPLATE_TYPES}.")
        
        config_obj = ConfigObject()

        config_obj.create_default_configs(config_types=config_types)

        self.write(f"The configuration files have been created. Please check the path: {CONFIG_PATH}.")

           
            
            


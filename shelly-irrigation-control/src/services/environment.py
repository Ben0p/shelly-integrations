import os
import argparse
from services.logging import LOGGER
from dotenv import load_dotenv




''' 
Module for initializing the environment
docker -> Loads variables from the OS environment (--env docker)
other -> Loads variables from a .env.x file (--env test)
For example "main.py --env test" loads ".env.test" file
.env files are excluded from git (except the example .env.example)
Again, "--env docker" loads from the OS environment, so define the variables in your docker-compose.yml

Types:
str: Normal string that gets stripped
int: Integer
float: Float
list[str]: list of strings only (env variable is csv - var1, var2, var3)
url: still a string but strips any trailing /
pass: A secret (str) that won't log to console
bool: Boolean, passes the string in to a bool type
dir: A directory, checks it exists, get's created if it doesn't
'''



class env:
    '''
    Environment initialization class. 
    Loads the variables from either .env files or the OS environment
    '''
    def __init__(self):
        self.load_definitions()
        self.parse_args()
        self.load_environment_type() 
        self.set_env()
        self.update_logging()
        LOGGER.info("Successfully loaded environment")


    def __str__(self) -> str:
        return self.ENVIRONMENT


    def load_definitions(self) -> None:
        '''
        Function to define the variables properties
        '''
        ##########################
        # Init props for linting #
        ##########################
        # General
        self.LOGGING_LEVEL = None
        self.POLLING_INTERVAL_SECONDS = None
        # File
        self.DEVICES_CONFIG_DIR = None
        self.DEVICES_CONFIG_FILE = None
        # Polling
        self.TIMEOUT = None
        self.FAILSAFE = None
        

        ########################
        #  Variable properties #
        ########################
        # Define the variable properties
        self.definitions = [
            # General
            {
                "name" : "LOGGING_LEVEL",
                "required" : False,
                "default" : "INFO",
                "type" : "str"
            },
            {
                "name" : "POLLING_INTERVAL_SECONDS",
                "required" : False,
                "default" : "5",
                "type" : "int"
            },
            # File
            {
                "name" : "DEVICES_CONFIG_DIR",
                "required" : False,
                "default" : "",
                "type" : "str"
            },
            {
                "name" : "DEVICES_CONFIG_FILE",
                "required" : False,
                "default" : "config.json",
                "type" : "str"
            },
            # Polling
            {
                "name" : "TIMEOUT",
                "required" : False,
                "default" : "1",
                "type" : "int"
            },
            {
                "name" : "FAILSAFE",
                "required" : False,
                "default" : "10",
                "type" : "int"
            }
        ]


    def parse_args(self) -> None:
        '''
        Load the environment type from the CLI "env" argument

        Args:
            None

        Returns:
            None
        '''
        # Setup argument parser
        parser = argparse.ArgumentParser(description="Run the script with specific environment settings.")
        parser.add_argument("--env", type=str, help="Specify the environment to use, e.g., 'test', 'dev', or 'docker'.")

        # Parse the arguments
        args, unknown = parser.parse_known_args()

        # Set the environment variable based on the argument
        self.ENVIRONMENT = args.env or "docker"


    def load_environment_type(self) -> None:
        '''
        Load the environment type from the environment param.

        Args:
            None

        Returns:
            None
        '''
        match self.ENVIRONMENT:
            case 'default':
                # Load test environment file by default
                self.ENVIRONMENT_FILE = '.env.test'
                self.SET = load_dotenv(self.ENVIRONMENT_FILE)
            case 'docker':
                self.ENVIRONMENT_FILE = "None"
                self.SET = True 
            case _:
                # Load environment file based on the environment name
                self.ENVIRONMENT_FILE = f'.env.{self.ENVIRONMENT}'
                self.SET = load_dotenv(self.ENVIRONMENT_FILE)


    def set_env(self) -> None:
        # Log the environment name
        LOGGER.info(f'Environment set to "{self.ENVIRONMENT}"')

        # Log warning if the environment isn't defined
        if self.ENVIRONMENT == "default":
            LOGGER.warning('Environment not defined with "--env", has been set to "test"')

        # Check if environment file loaded successfully, no point continuing if it isn't
        # Only applicable when the envionment isn't docker
        if not self.SET:
            LOGGER.critical("Unable to load environment file.")
            LOGGER.critical(f'The enviornment is set to "{self.ENVIRONMENT}" but unable to load the "{self.ENVIRONMENT_FILE}" file.')
            exit(1)
        
        # Iterate variables defined in self.definitions
        var_missing = False
        for var in self.definitions:
            # Check if variable is required
            if var['required']:
                # If a required variable is missing
                if var['name'] not in os.environ:
                    LOGGER.critical(f'Required environment variable "{var["name"]}" not defined')
                    var_missing = True
                # If a required variable is blank
                elif not os.environ[var['name']]:
                    LOGGER.critical(f'Required environment variable "{var["name"]}" is blank')
                    var_missing = True
            # If variable not required
            else:
                # If an optional variable is missing
                if var['name'] not in os.environ:
                    LOGGER.warning(f'Optional environment variable "{var["name"]}" not defined, setting to default value "{var["default"]}"')
                # If an optional variable is blank
                elif not os.environ[var['name']]:
                    LOGGER.warning(f'Optional environment variable "{var["name"]}" is blank, setting to default value "{var["default"]}"')

            # Load value from OS environment else load default value defined in json
            value = os.environ.get(var['name'], var['default'])
            # Handle when variable exists but it is blank
            if not value:
                value = var["default"]

            if value:
                try:
                    value = self.process_value(value, var)
                    setattr(self, var['name'], value)
                except Exception as e:
                    LOGGER.critical(e)
                    LOGGER.critical(f'Unable to process environment variable "{var["name"]}"')
                    var_missing = True
                # Log variable
                if not var['type'] == 'pass':
                    if var['type'] == 'str':
                        LOGGER.info(f'{var["name"]}="{value}"')
                    if not var['type'] == 'str':
                        LOGGER.info(f'{var["name"]}={value}')

                # Don't log passwords / API keys
                if var['type'] == 'pass':
                    LOGGER.info(f"{var['name']}=*redacted*")

        # Log critical error and exit if a required variable is missing
        if var_missing:
            LOGGER.critical("Required environment variable(s) missing or unable to process.")
            if self.ENVIRONMENT == 'docker':
                LOGGER.critical("Ensure all required variables are correct in the Docker environment")
            else:
                LOGGER.critical("Ensure all required variables are correct in the .env file")
            LOGGER.critical("Exiting...")
            exit(1)
    

    def process_value(
            self,
            value: str | int | float,
            var: dict
        ) -> int | str | float | list[str] | bool:
        '''
        Check and convert variable type

        Args:
            value (str): The value either from OS environment or default
            var (dict): The variable object from vars.json 

        Returns:
            Union(int, str, float, list[str], bool): The converted variable to the type
        '''
        
        match var['type']:
            case 'str' | 'pass':
                value = str(value)
                value = value.rstrip()
            case 'int':
                value = int(value)
            case 'float':
                value = float(value)
            case 'list':
                # Assuming list of strings separated by comma (,)
                value = value.split(',')
            case 'url':
                value = value.rstrip().lower()
                value = value.rstrip('/')
            case 'bool':
                if value.lower() in ['true', 't', 'tr', 'yes', 'y', 'nahyeh', 'whynot', 'please']:
                    LOGGER.debug(f'"{value}" matched to be the boolean True')
                    value = True
                else:
                    LOGGER.debug(f'"{value}" matched to be the boolean False')
                    value = False
            case 'dir':
                # Check if file is a directory
                if os.path.isdir(value):
                    LOGGER.debug(f'"{value}" directory exists')
                else:
                    os.mkdir(value)
                    LOGGER.debug(f"Created directory {value}")

        # If no matches, it'll just retun as is
        return value


    def update_logging(self) -> None:
        '''
        Update the logging level to what is set in the environment. Defaults to "INFO".

        Args:
            None

        Returns:
            None
        '''
        # Update the logger
        if self.LOGGING_LEVEL.lower() not in ['debug', 'info', 'error', 'warning', 'critical']:
            LOGGER.warning(f'Unable to determine logging level from "{self.LOGGING_LEVEL}"')
            LOGGER.warning('Setting the logging level to INFO')
            self.LOGGING_LEVEL = 'INFO'

        LOGGER.setLevel(self.LOGGING_LEVEL)
        LOGGER.info(f"Updated logging level to {self.LOGGING_LEVEL} from the environment.")



# Initialize environment class and load to ENV
# Use "from services.environmentservice import ENV"
# Only Initialized on the first import, subsequent imports are cached
ENV = env()
import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme
import datetime
import pytz
import os



'''
Service for handling the logging initialization and format.
Includes the beautiful colourized styling with RichHandler.
In Docker, set tty: true to get the colours to work.
'''



def format_time(time: datetime.datetime) -> str:
    '''
    Takes a datetime.datetime object, adds the timezone from the environment and a "|" delimeter,
    then returns a formatted string. The delimeter makes the final log output look better.

    Args:
        time (datetime.datetime): The datetime object to format 

    Returns:
        str: The string formatted time stamp
    '''
    # Temporarily set the timezone to UTC if the environment hasn't loaded yet
    if "TIMEZONE" in os.environ:
        timezone = pytz.timezone(os.environ['TIMEZONE'])
    else:
        timezone = pytz.timezone('UTC')

    time = time.astimezone(timezone)
    time = time.isoformat(timespec='milliseconds')
    return f"{time} |"


def init_logging(logging_level: str = 'INFO') -> logging.Logger:
    '''
    Takes the logging level, usually from the environment, then initialises the logging object.
    Returns the configured logging.Logger object.

    Args:
        logging_level (str): The logging level (any case)

    Returns:
        logging.Logger: The configured logging.Logger object
    '''
    # Configure the console colour theme
    console = Console(
        theme=Theme(
            {
                "logging.level.info": "bright_cyan",
                "logging.level.warning": "bright_yellow",
                "logging.level.error": "bright_magenta",
                "logging.level.critical": "bright_red",
                "logging.level.debug": "bright_green",
                "log.time" : "white",
                "repr.url" : "bright_blue"
            }
        )
    )

    # Set logging level
    match logging_level.lower().strip():
        case 'debug':
            level = logging.DEBUG
        case 'info':
            level = logging.INFO
        case 'warning':
            level = logging.WARNING
        case 'error':
            level = logging.ERROR
        case 'critical':
            level = logging.CRITICAL
        case _:
            level = logging.INFO

    # Inititialize the Rich Handler
    rich = RichHandler(
        show_path=False,
        show_time=True,
        show_level=True,
        omit_repeated_times=False,
        console=console,
        log_time_format=format_time
    )

    # Set up logging
    logging.basicConfig(
        level=level,
        handlers=[rich]
    )

    # Configure then get the logger
    rich_handler = logging.getLogger().handlers[0]
    rich_handler.setFormatter(logging.Formatter("| %(message)s"))
    logger = logging.getLogger()

    # Log status
    logging_level_name = logging.getLevelName(logger.level)
    logger.info(f'Logging level temporarily set to "{logging_level_name}"')

    # Log test levels
    if logging_level_name == "DEBUG":
        logger.debug("DEBUG test")
        logger.info("INFO test")
        logger.error("ERROR test")
        logger.warning("WARNING test")
        logger.critical("CRITICAL test")

    return logger


# Set initial logging level. Updated later in the environment initialization.
LOGGER = init_logging('DEBUG')
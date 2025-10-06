from services.environment import ENV
from services.logging import LOGGER
from services import loaddevices
import os
from pathlib import Path





def main():
    '''
    Main loop function
    '''
    LOGGER.warning("First script run.")
    # Load devices
    devices = loaddevices.FromJson()
    irrigation_controllers = devices.irrigation_controllers
    pump = devices.pump
    
    

    



if __name__ == "__main__":
    main()
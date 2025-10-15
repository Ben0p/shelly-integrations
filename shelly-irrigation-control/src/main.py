from services.environment import ENV
from services.logging import LOGGER
from services import loaddevices
import os
from pathlib import Path
from pprint import pprint

from devices.shellypro1pm import ShellyPro1Pm



def main():
    '''
    Main loop function
    '''
    LOGGER.warning("First script run.")
    # Load devices
    devices = loaddevices.FromJson()
    irrigation_controllers = devices.irrigation_controllers
    pump = devices.pump
    pump = ShellyPro1Pm(pump)

    # pprint(pump.as_dict())
    print(pump.relay_on_timer())
    

    



if __name__ == "__main__":
    main()
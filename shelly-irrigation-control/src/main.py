from services.environment import ENV
from services.logging import LOGGER
from services import loaddevices
import os
from pathlib import Path
from pprint import pprint

from devices.shellypro1pm import ShellyPro1Pm
from devices.fk06x import Fk06x



def main():
    '''
    Main loop function
    '''
    LOGGER.warning("First script run.")
    # Load devices
    devices = loaddevices.FromJson()
    irrigation_controllers = devices.irrigation_controllers
    irrigation_controllers = [Fk06x(irrigation_controller) for irrigation_controller in irrigation_controllers]
    pump = devices.pump
    pump = ShellyPro1Pm(pump)
    

    # pprint(pump.as_dict())
    # print(pump.relay_on_timer())
    pprint(irrigation_controllers[0].as_dict())
    

    



if __name__ == "__main__":
    main()
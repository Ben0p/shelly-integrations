from services.environment import ENV
from services.logging import LOGGER
from services import loaddevices
import os
from pathlib import Path
from pprint import pprint
import time


def main():
    '''
    Main loop function
    '''
    LOGGER.warning("First script run.")
    # Load devices
    devices = loaddevices.FromJson()
    irrigation_controllers = devices.irrigation_controllers
    pump = devices.pump
    

    # pprint(pump.as_dict())
    # print(pump.relay_on_timer())
    # pprint(irrigation_controllers[0].as_dict())
    while True:
        pump_on = False
        for irrigation_controller in irrigation_controllers:
            for zone in irrigation_controller.boolean_statuses:
                if zone.value:
                    pump_relay = pump.relay_on_timer()
                    if pump_relay.ison:
                        pump_on = True
                        break
            if pump_on:
                break
        print(f"Pump is on: {pump_on}")
        time.sleep(ENV.POLLING_INTERVAL_SECONDS)
    

    



if __name__ == "__main__":
    main()

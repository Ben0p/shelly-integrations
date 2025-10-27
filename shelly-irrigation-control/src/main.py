from services.environment import ENV
from services.logging import LOGGER
from services import loaddevices
import time



'''
Main entrypoint module for the Shelly Irrigation Control
Loads shelly devices (fk06x and Pro1PM) from .json config
Simply checks if any irrigation zone is active, then turns on the Pro1PM relay
Uses the relay on timer as a failsafe. No need to trigger the relay off.
'''



def main():
    '''
    Main loop function
    '''
    LOGGER.warning("First script run.")
    # Load devices
    devices = loaddevices.FromJson()
    irrigation_controllers = devices.irrigation_controllers
    pump = devices.pump
    pump_state: bool = None
    some_error: bool = False
    error_state = None
    
    while True:
        for irrigation_controller in irrigation_controllers:
            if irrigation_controller.zone_active:
                pump.relay_on_timer()
                if pump.is_active:
                    break
            if irrigation_controller.has_error:
                LOGGER.error(irrigation_controller.last_error_msg)
                some_error = True
            else:
                some_error = False
        if pump_state != pump.is_active:
            if pump.is_active:
                LOGGER.info(f"The pump is now running...")
            else:
                LOGGER.info(f"The pump has stopped")
            pump_state = pump.is_active
        if pump.has_error:
            LOGGER.error(pump.last_error_msg)
            some_error = True
        else:
            some_error = False

        if error_state != some_error:
            if some_error:
                LOGGER.error("There was some error, ignoring and trying again...")
                
        error_state = some_error
        time.sleep(ENV.POLLING_INTERVAL_SECONDS)
    

    



if __name__ == "__main__":
    main()

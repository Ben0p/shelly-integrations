from components.device import Device
from components.sysGetStatus import SysGetStatus
from components.switchGetConfig import SwitchGetConfig
from components.switchGetStatus import SwitchGetStatus
from components.relay import Relay
import requests
import time



'''
Class for a Shelly Pro 1PM
'''



class ShellyPro1Pm:
    def __init__(self, device: Device):
        self._device: Device = device
        # Sys.GetStatus
        self._sys_get_status_cache: SysGetStatus = None
        self._sys_get_status_polled_time: float = 0.0
        # Switch.GetConfig
        self._switch_get_config_cache: SwitchGetConfig = None
        self._switch_get_config_polled_time: float = 0.0
        # Switch.GetStatus
        self._switch_get_status_cache: SwitchGetStatus = None
        self._switch_get_status_polled_time: float = 0.0
        # Relay
        self._relay_response_cache: Relay = None
        self._relay_response_polled_time: float = 0.0


    
    def __string__(self) -> str:
        return str(self.as_dict())
        
        
    def as_dict(self) -> dict:
        return {
            'device' : self.device.as_dict(),
            'sys' : self.sys.as_dict(),
            'switch_0_config' : self.switch_0_config.as_dict(),
            'switch_0_status' : self.switch_0_status.as_dict()
        }
        
    
    def _sys_get_status(self):
        if (time.time() - self._sys_get_status_polled_time) > self.device.interval_seconds:
            data = requests.get(f"http://{self.device.ip}/rpc/Sys.GetStatus")
            self._sys_get_status_cache = SysGetStatus(data.json())
            self._sys_get_status_polled_time = time.time()
            

    def _switch_get_config(self, id: int):
        if (time.time() - self._switch_get_config_polled_time) > self.device.interval_seconds:
            data = requests.get(f"http://{self.device.ip}/rpc/Switch.GetConfig?id={id}")
            self._switch_get_config_cache = SwitchGetConfig(data.json())
            self._switch_get_config_polled_time = time.time()


    def _switch_get_status(self, id: int):
        if (time.time() - self._switch_get_status_polled_time) > self.device.interval_seconds:
            data = requests.get(f"http://{self.device.ip}/rpc/Switch.GetStatus?id={id}")
            self._switch_get_status_cache = SwitchGetStatus(data.json())
            self._switch_get_status_polled_time = time.time()

    
    def relay_on_timer(self) -> Relay:
        '''
        Turns on the Shelly Pro1PM relay with a timer in seconds \n
        The Shelly Pro1PM only has one relay \n
        The timer seconds is defined in the .json devices configuration file \n
        The relay will turn off after the timer seconds has elapsed
        

        Args:
            None

        Returns:
            Relay: Relay class as the response
        
        Raises:
            HttpError: If there is a request http error
        '''
        if (time.time() - self._relay_response_polled_time) > self.device.interval_seconds:
            response = requests.get(f"http://{self.device.ip}/relay/0?turn=on&timer={self.device.failsafe_seconds}")
            response.raise_for_status()
            self._relay_response_cache = Relay(response.json())
            self._relay_response_polled_time = time.time()
        return self._relay_response_cache
            

    @property
    def can_poll(self) -> bool:
        return (time.time() - self._switch_get_status_polled_time) > self.device.interval_seconds
    
    
    @property
    def device(self) -> Device:
        return self._device

    
    @property
    def sys(self) -> SysGetStatus:
        self._sys_get_status()
        return self._sys_get_status_cache


    @property
    def switch_0_config(self) -> SwitchGetConfig:
        self._switch_get_config(0)
        return self._switch_get_config_cache


    @property
    def switch_0_status(self) -> SwitchGetStatus:
        self._switch_get_status(0)
        return self._switch_get_status_cache

   
    @property
    def relay(self) -> Relay:
        return self._relay_response_cache
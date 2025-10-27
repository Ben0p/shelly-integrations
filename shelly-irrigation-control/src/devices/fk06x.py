from components.device import Device
from components.sysGetStatus import SysGetStatus
from components.boolean.status import BooleanStatus
import requests
import time



'''
Class for a Shelly Pro 1PM
'''



class Fk06x:
    def __init__(self, device: Device):
        self._device: Device = device
        # Sys.GetStatus
        self._sys_get_status_cache: SysGetStatus = None
        self._sys_get_status_polled_time: float = 0.0
        # Boolean.GetStatus
        self._boolean_keys: list[int] = [200, 201, 202, 203, 204, 205]
        self._boolean_get_status_caches: list[BooleanStatus] = [None, None, None, None, None, None]
        self._boolean_get_status_polled_times: list[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # Error
        self._has_error: bool = False
        self._last_error_msg: str = None


    
    def __string__(self) -> str:
        return str(self.as_dict())
        
        
    def as_dict(self) -> dict:
        return {
            'device' : self.device.as_dict(),
            'sys' : self.sys.as_dict(),
            'booleans' : [boolean_status.as_dict() for boolean_status in self.boolean_statuses],
            'zone_active' : self.zone_active,
            'is_error' : self.is_error,
            'last_error_msg' : self.last_error_msg
        }
        
    
    def _sys_get_status(self):
        if (time.time() - self._sys_get_status_polled_time) > self.device.interval_seconds:
            data = requests.get(f"http://{self.device.ip}/rpc/Sys.GetStatus")
            self._sys_get_status_cache = SysGetStatus(data.json())
            self._sys_get_status_polled_time = time.time()


    def _bool_get_statuses(self):
        for idx, key in enumerate(self._boolean_keys):
            if (time.time() - self._boolean_get_status_polled_times[idx]) > self.device.interval_seconds:
                try:
                    data = requests.get(f"http://{self.device.ip}/rpc/Boolean.GetStatus?id={key}")
                    self._boolean_get_status_caches[idx] = BooleanStatus(data.json())
                    self._boolean_get_status_polled_times[idx] = time.time()
                    self._has_error = False
                except Exception as e:
                    self._last_error_msg = e
                    self._has_error = True
        
    
    @property
    def device(self) -> Device:
        return self._device

    
    @property
    def sys(self) -> SysGetStatus:
        self._sys_get_status()
        return self._sys_get_status_cache
    
    
    @property
    def boolean_statuses(self) -> list[BooleanStatus]:
        self._bool_get_statuses()
        return self._boolean_get_status_caches
    
    
    @property
    def zone_active(self) -> bool:
        zone_states = [boolean.value for boolean in self.boolean_statuses]
        return any(zone_states)
    
    
    @property
    def has_error(self) -> bool:
        return self._has_error
    
    
    @property
    def last_error_msg(self) -> str:
        return self._last_error_msg
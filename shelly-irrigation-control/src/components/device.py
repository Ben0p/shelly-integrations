from utils import normalize



'''
Shelly generic device class
'''



class Device:
    def __init__(self, device: dict):
        self._device: dict = device


    def __str__(self):
        return str(self.as_dict())

 
    def as_dict(self):
        return {
            "name" : self.name,
            "ip" : self.ip,
            "model" : self.model,
            "interval_seconds" : self.interval_seconds
        }
        

    @property
    def name(self) -> str:
        return normalize.to_str_or_none(self._device.get("name"))


    @property
    def ip(self) -> str:
        return normalize.to_str_or_none(self._device.get("ip"))


    @property
    def model(self) -> str:
        return normalize.to_str_or_none(self._device.get("model"))


    @property
    def interval_seconds(self) -> int:
        return normalize.to_int_or_none(self._device.get("interval_seconds"))
    
    
    @property
    def failsafe_seconds(self) -> int:
        return normalize.to_int_or_none(self._device.get("failsafe_seconds"))
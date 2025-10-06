from .device import Device



'''
Class for a Shelly Pro 1PM (pump relay)
'''



class ShellyPro1Pm:
    def __init__(self, device: Device):
        self.device: Device = device
        self.ip: str = device.ip
        self.name: str = device.name
        self.model: str = device.model
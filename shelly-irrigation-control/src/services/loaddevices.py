from services.environment import  ENV
import json
import re
from pathlib import Path
from components.device import Device



'''
Service to load a list of Shelly FK-06X irrigation controllers from config.json
'''



class FromJson:
    VALID_MODELS = ["fk-06x", "shellypro1pm"]
    IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\- ]+$")


    def __init__(self):
        self.file_path: Path = None
        self.irrigation_controllers: list[Device] = []
        self.pump: Device = None
        self.invalid_devices: list[Device] = []
        self._get_file_path()
        self.devices: dict = self._load_devices()
        self._load_irrigation_controllers()
        self._load_pump_relay()

    
    def _get_file_path(self):
        base_dir = Path(ENV.DEVICES_CONFIG_DIR) if ENV.DEVICES_CONFIG_DIR else Path()
        self.file_path = base_dir / ENV.DEVICES_CONFIG_FILE


    def _load_devices(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)


    def _is_valid_ip(self, ip):
        return bool(self.IP_REGEX.match(ip))


    def _is_valid_model(self, model):
        return model in self.VALID_MODELS


    def _is_valid_name(self, name):
        return bool(self.NAME_REGEX.match(name))


    def _load_irrigation_controllers(self):
        for irrigation_controller in self.devices['irrigation_controllers']:
            ic: Device = Device(irrigation_controller)
            if self._is_valid_ip(ic.ip) and self._is_valid_model(ic.model) and self._is_valid_name(ic.name):
                self.irrigation_controllers.append(ic)
            else:
                self.invalid_devices.append(ic)
            
        if len(self.irrigation_controllers) < 1:
            raise ValueError("No valid irrigation controllers")
        

    def _load_pump_relay(self):
        self.pump: Device = Device(self.devices.get("pump_relay"))
        if not self._is_valid_ip(self.pump.ip) and self._is_valid_model(self.pump.model) and self._is_valid_name(self.pump.name):
            raise ValueError("Invalid pump")
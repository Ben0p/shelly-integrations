from services.environment import ENV
import json
import re
from pathlib import Path
from typing import Any, Callable
from components import Device
from devices import Fk06x, ShellyPro1Pm



'''
Service to load Shelly devices from config.json
'''



class FromJson:
    MODEL_FACTORIES: dict[str, Callable[[Device], Any]] = {
        "fk-06x": Fk06x,
        "shellypro1pm": ShellyPro1Pm
    }
    IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\- ]+$")


    def __init__(self):
        self.file_path: Path = None
        self.irrigation_controllers: list[Fk06x] = []
        self.pump: ShellyPro1Pm = None
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
        return isinstance(ip, str) and bool(self.IP_REGEX.match(ip))


    def _is_valid_model(self, model):
        return model in self.MODEL_FACTORIES


    def _is_valid_name(self, name):
        return isinstance(name, str) and bool(self.NAME_REGEX.match(name))


    def _load_irrigation_controllers(self):
        for irrigation_controller in self.devices['irrigation_controllers']:
            instance = self._create_device_instance(irrigation_controller)
            if instance:
                self.irrigation_controllers.append(instance)
            
        if len(self.irrigation_controllers) < 1:
            raise ValueError("No valid irrigation controllers")
        

    def _load_pump_relay(self):
        pump_config = self.devices.get("pump_relay")
        if not pump_config:
            return

        pump_instance = self._create_device_instance(pump_config)
        if not pump_instance:
            raise ValueError("Invalid pump")
        self.pump = pump_instance


    def _create_device_instance(self, device_config: dict) -> Any | None:
        device = Device(device_config)
        if not (self._is_valid_ip(device.ip) and self._is_valid_model(device.model) and self._is_valid_name(device.name)):
            self.invalid_devices.append(device)
            return None

        factory = self.MODEL_FACTORIES.get(device.model)
        if not factory:
            self.invalid_devices.append(device)
            return None

        return factory(device)

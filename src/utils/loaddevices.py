import json
import re

class FromJson:
    VALID_MODELS = ["shelly4em"]
    IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\- ]+$")

    def __init__(self, file_path):
        self.file_path = file_path
        self.devices = self._load_devices()
        self.valid_devices = []
        self.invalid_devices = []

    def _load_devices(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def _is_valid_ip(self, ip):
        return bool(self.IP_REGEX.match(ip))

    def _is_valid_model(self, model):
        return model in self.VALID_MODELS

    def _is_valid_name(self, name):
        return bool(self.NAME_REGEX.match(name))

    def validate_devices(self):

        for device in self.devices:
            ip = device.get("ip")
            model = device.get("model")
            name = device.get("name")
            if self._is_valid_ip(ip) and self._is_valid_model(model) and self._is_valid_name(name):
                self.valid_devices.append(device)
            else:
                self.invalid_devices.append(device)
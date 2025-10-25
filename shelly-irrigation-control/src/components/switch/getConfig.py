from utils import normalize



class SwitchGetConfig:
    '''
    Class for the shelly Switch.GetConfig component
    '''
    def __init__(self, data: dict):
        self._data: dict = data


    def __str__(self):
        return str(self.as_dict)


    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "in_mode": self.in_mode,
            "in_locked": self.in_locked,
            "initial_state": self.initial_state,
            "auto_on": self.auto_on,
            "auto_on_delay": self.auto_on_delay,
            "auto_off": self.auto_off,
            "auto_off_delay": self.auto_off_delay,
            "autorecover_voltage_errors": self.autorecover_voltage_errors,
            "power_limit": self.power_limit,
            "voltage_limit": self.voltage_limit,
            "undervoltage_limit": self.undervoltage_limit,
            "current_limit": self.current_limit,
            "reverse": self.reverse,
            "input_id" : self.input_id
        }
        
        
    @property
    def id(self) -> int:
        return normalize.to_int_or_none(self._data.get('id', None))


    @property
    def name(self) -> str:
        return normalize.to_str_or_none(self._data.get('name', None))


    @property
    def in_mode(self) -> str:
        return normalize.to_str_or_none(self._data.get('in_mode', None))


    @property
    def in_locked(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('in_locked', None))


    @property
    def initial_state(self) -> str:
        return normalize.to_str_or_none(self._data.get('initial_state', None))


    @property
    def auto_on(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('auto_on', None))


    @property
    def auto_on_delay(self) -> int:
        return normalize.to_int_or_none(self._data.get('auto_on_delay', None))


    @property
    def auto_off(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('auto_off', None))


    @property
    def auto_off_delay(self) -> int:
        return normalize.to_int_or_none(self._data.get('auto_off_delay', None))


    @property
    def autorecover_voltage_errors(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('autorecover_voltage_errors', None))


    @property
    def power_limit(self) -> int:
        return normalize.to_int_or_none(self._data.get('power_limit', None))


    @property
    def voltage_limit(self) -> int:
        return normalize.to_int_or_none(self._data.get('voltage_limit', None))


    @property
    def undervoltage_limit(self) -> int:
        return normalize.to_int_or_none(self._data.get('undervoltage_limit', None))


    @property
    def current_limit(self) -> int:
        return normalize.to_int_or_none(self._data.get('current_limit', None))


    @property
    def reverse(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('reverse', None))


    @property
    def input_id(self) -> int:
        return normalize.to_int_or_none(self._data.get('input_id', None))
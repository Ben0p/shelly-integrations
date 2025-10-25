from utils import normalize
from ..aenergy import Aenergy
from ..retAenergy import RetAenergy
from ..temperature import Temperature



class SwitchGetStatus:
    '''
    Class for the shelly Switch.GetStatus component
    '''
    def __init__(self, data: dict):
        self._data: dict = data


    def __str__(self):
        return str(self.as_dict)


    def as_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "output": self.output,
            "apower": self.apower,
            "voltage": self.voltage,
            "current": self.current,
            "freq": self.freq,
            "aenergy": self.aenergy.as_dict(),
            "ret_aenergy": self.ret_aenergy.as_dict(),
            "temperature": self.temperature.as_dict()
        }
        
        
    @property
    def id(self) -> int:
        return normalize.to_int_or_none(self._data.get('id'))


    @property
    def source(self) -> str:
        return normalize.to_str_or_none(self._data.get('source'))


    @property
    def output(self) -> bool:
        return normalize.to_bool_or_none(self._data.get('output'))


    @property
    def apower(self) -> float:
        return normalize.to_float_or_none(self._data.get('apower'))


    @property
    def voltage(self) -> float:
        return normalize.to_float_or_none(self._data.get('voltage'))


    @property
    def freq(self) -> float:
        return normalize.to_float_or_none(self._data.get('freq'))


    @property
    def current(self) -> float:
        return normalize.to_float_or_none(self._data.get('current'))


    @property
    def pf(self) -> float:
        return normalize.to_float_or_none(self._data.get('pf'))


    @property
    def aenergy(self) -> Aenergy:
        return Aenergy(self._data.get('aenergy'))


    @property
    def ret_aenergy(self) -> RetAenergy:
        return RetAenergy(self._data.get('ret_aenergy'))


    @property
    def temperature(self) -> Temperature:
        return Temperature(self._data.get('temperature'))
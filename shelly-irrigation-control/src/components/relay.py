from utils import normalize



class Relay:
    def __init__(self, data: dict):
        self._data: dict = data
    
    
    def __str__(self) -> str:
        return str(self.as_dict())


    def as_dict(self) -> dict:
        return {
            "ison" : self.ison,
            "has_timer" : self.has_timer,
            "timer_started_at" : self.timer_started_at,
            "timer_duration" : self.timer_duration,
            "timer_remaining" : self.timer_remaining,
            "overpower" : self.overpower,
            "source" : self.source
        }
    
    
    @property
    def ison(self) -> bool | None:
        return normalize.to_bool_or_none(self._data.get("ison"))


    @property
    def has_timer(self) -> bool | None:
        return normalize.to_bool_or_none(self._data.get("has_timer"))
    

    @property
    def timer_started_at(self) -> int | None:
        return normalize.to_int_or_none(self._data.get("timer_started_at"))


    @property
    def timer_duration(self) -> float | None:
        return normalize.to_float_or_none(self._data.get("timer_duration"))


    @property
    def timer_remaining(self) -> float | None:
        return normalize.to_float_or_none(self._data.get("timer_remaining"))


    @property
    def overpower(self) -> bool | None:
        return normalize.to_bool_or_none(self._data.get("overpower"))


    @property
    def source(self) -> bool | None:
        return normalize.to_str_or_none(self._data.get("source"))
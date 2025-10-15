from utils import normalize



class Aenergy:
    def __init__(self, data: dict):
        self._data: dict = data
    
    
    def __str__(self) -> str:
        return str(self.as_dict())


    def as_dict(self) -> dict:
        return {
            "total" : self.total,
            "by_minute" : self.by_minute,
            "minute_ts" : self.minute_ts
        }
    
    
    @property
    def total(self) -> float | None:
        return normalize.to_float_or_none(self._data.get("total", None))


    @property
    def by_minute(self) -> list[float]:
        return normalize.to_list_of_float(self._data.get("by_minute", None))
    

    @property
    def minute_ts(self) -> int | None:
        return normalize.to_int_or_none(self._data.get("minute_ts", None))
from utils import normalize



class BooleanStatus:
    def __init__(self, data: dict):
        self._data: dict = data
    
    
    def __str__(self) -> str:
        return str(self.as_dict())


    def as_dict(self) -> dict:
        return {
            "value" : self.value,
            "source" : self.source,
            "last_update_ts" : self.last_update_ts
        }
    
    
    @property
    def value(self) -> bool | None:
        return normalize.to_bool_or_none(self._data.get("value"))


    @property
    def source(self) -> str:
        return normalize.to_str_or_none(self._data.get("source"))
    

    @property
    def last_update_ts(self) -> int | None:
        return normalize.to_int_or_none(self._data.get("last_update_ts"))
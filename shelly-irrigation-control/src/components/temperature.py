from utils import normalize



class Temperature:
    def __init__(self, data: dict):
        self._data: dict = data
    
    
    def __str__(self) -> str:
        return str(self.as_dict())


    def as_dict(self) -> dict:
        return {
            "tC" : self.tC,
            "tF" : self.tF
        }
    
    
    @property
    def tC(self) -> float | None:
        return normalize.to_float_or_none(self._data.get("tC", None))


    @property
    def tF(self) -> float | None:
        return normalize.to_float_or_none(self._data.get("tF", None))
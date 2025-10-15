



class Update:
    def __init__(self, data: dict):
        self._data: dict = data
    

    @property
    def version(self) -> str:
        return self._data.get("version", None)
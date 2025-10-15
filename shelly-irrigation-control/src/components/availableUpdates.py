from .update import Update



class AvailableUpdates:
    def __init__(self, data: dict):
        self._data: dict = data
    

    @property
    def stable(self) -> Update:
        return Update(self._data.get("stable", None))
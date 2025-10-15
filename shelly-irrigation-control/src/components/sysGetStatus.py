from .availableUpdates import AvailableUpdates



class SysGetStatus:
    '''
    Class for the shelly Sys.GetStatus component
    '''
    def __init__(self, data: dict):
        self._data: dict = data


    def __str__(self):
        return str(self.as_dict)


    def as_dict(self):
        return {
            "mac": self.mac,
            "restart_required": self.restart_required,
            "time": self.time,
            "unixtime": self.unixtime,
            "last_sync_ts": self.last_sync_ts,
            "uptime": self.uptime,
            "ram_size": self.ram_size,
            "ram_free": self.ram_free,
            "fs_size": self.fs_size,
            "fs_free": self.fs_free,
            "cfg_rev": self.cfg_rev,
            "kvs_rev": self.kvs_rev,
            "schedule_rev": self.schedule_rev,
            "webhook_rev": self.webhook_rev,
            "btrelay_rev": self.btrelay_rev,
            "available_updates" : self.available_updates
        }
        
        
    @property
    def mac(self) -> str:
        return self._data.get('mac', None)


    @property
    def restart_required(self) -> bool:
        return self._data.get('restart_required', None)
    

    @property
    def time(self) -> str:
        return self._data.get('time', None)
    

    @property
    def unixtime(self) -> int:
        return self._data.get('unixtime', None)
    

    @property
    def last_sync_ts(self) -> int:
        return self._data.get('last_sync_ts', None)
    

    @property
    def uptime(self) -> int:
        return self._data.get('uptime', None)
    

    @property
    def ram_size(self) -> int:
        return self._data.get('ram_size', None)
    

    @property
    def ram_free(self) -> int:
        return self._data.get('ram_free', None)


    @property
    def fs_size(self) -> int:
        return self._data.get('fs_size', None)


    @property
    def fs_free(self) -> int:
        return self._data.get('fs_free', None)
    

    @property
    def cfg_rev(self) -> int:
        return self._data.get('cfg_rev', None)


    @property
    def kvs_rev(self) -> int:
        return self._data.get('kvs_rev', None)


    @property
    def schedule_rev(self) -> int:
        return self._data.get('schedule_rev', None)


    @property
    def webhook_rev(self) -> int:
        return self._data.get('webhook_rev', None)


    @property
    def btrelay_rev(self) -> int:
        return self._data.get('btrelay_rev', None)


    @property
    def available_updates(self) -> AvailableUpdates:
        return self._data.get('available_updates', None)
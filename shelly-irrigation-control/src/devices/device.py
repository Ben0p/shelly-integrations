



class Device:
    def __init__(self, device: dict):
        self.name: str = device.get("name", None)
        self.ip: str = device.get("ip", None)
        self.model: str = device.get("model", None)


    def __str__(self):
        return str(self.as_dict())

 
    def as_dict(self):
        return {
            "name" : self.name,
            "ip" : self.ip,
            "model" : self.model
        }
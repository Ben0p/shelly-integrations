import requests
import json



class ShellyPro1Pm:
    def __init__(self, ip: str, name: str):
        self.ip_address = ip
        self.name = name
        self.model = "shellypro1pm"


    def get_point(self):
        self.get_all()
        self.create_point()
        return self.point
        
        
    def get_all(self):
        try:
            self.info = self.get_info()
            self.system = self.get_system()
            self.wifi = self.get_wifi()
            self.inputs = self.get_inputs()
            self.switch = self.get_switch()
            self.all = {
                'info' : self.info,
                'system' : self.system,
                'wifi' : self.wifi,
                'inputs' : self.inputs,
                'switch' : self.switch
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Shelly Pro 1 PM data: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


    def get_info(self):
        '''
        Fetches the basic information from the /shelly endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response from the /shelly endpoint.
        '''
        response = requests.get(f"http://{self.ip_address}/shelly")
        response.raise_for_status()
        data = response.json()
        data['ip'] = self.ip_address,
        data['user_defined_name'] = self.name
        return data


    def get_system(self):
        response = requests.get(f"http://{self.ip_address}/rpc/Sys.GetStatus")
        response.raise_for_status()
        data = response.json()
        data['available_updates'] = bool(data['available_updates'])
        return data
    
    
    def get_wifi(self):
        response = requests.get(f"http://{self.ip_address}/rpc/WiFi.GetStatus")
        response.raise_for_status()
        data = response.json()
        data["sta_ip6"] = data["sta_ip6"][0]
        return data
           

    def get_inputs(self):
        inputs = []
        for input_id in [0, 1]:
            response = requests.get(f"http://{self.ip_address}/rpc/Input.GetStatus?id={input_id}")
            response.raise_for_status()
            data = response.json()
            inputs.append(data)

        return {
            "input_0" : inputs[0]["state"],
            "input_1" : inputs[1]["state"]
        }


    def get_switch(self):
        response = requests.get(f"http://{self.ip_address}/rpc/Switch.GetStatus?id=0")
        response.raise_for_status()
        data = response.json()
        return {
            "id" : data["id"],
            "source" : data["source"],
            "output" : data["output"],
            "apower" : data["apower"],
            "voltage" : data["voltage"],
            "freq" : data["freq"],
            "current" : data["current"],
            "pf" : data["pf"],
            "aenergy_total" : data["aenergy"]["total"],
            "aenergy_by_minute_0" : data["aenergy"]["by_minute"][0],
            "aenergy_by_minute_1" : data["aenergy"]["by_minute"][1],
            "aenergy_by_minute_2" : data["aenergy"]["by_minute"][2],
            "aenergy_minute_ts" : data["aenergy"]["minute_ts"],
            "ret_aenergy_total" : data["ret_aenergy"]["total"],
            "ret_aenergy_by_minute_0" : data["ret_aenergy"]["by_minute"][0],
            "ret_aenergy_by_minute_1" : data["ret_aenergy"]["by_minute"][1],
            "ret_aenergy_by_minute_2" : data["ret_aenergy"]["by_minute"][2],
            "ret_aenergy_minute_ts" : data["ret_aenergy"]["minute_ts"],
            "temperature_tC" : data["temperature"]["tC"],
            "temperature_tF" : data["temperature"]["tF"]
        }
            
            
    def create_point(self):
        self.point =  {
            "measurement": "shellypro1pm",
            "tags": {
                **self.info
            },
            "fields": {
                **self.system,
                **self.wifi,
                **self.inputs,
                **self.switch
            }
        }
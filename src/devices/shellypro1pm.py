import requests
import json



'''
Shelly Pro 1 PM device class
'''



class ShellyPro1Pm:
    def __init__(self, ip: str, name: str):
        self.ip_address = ip
        self.name = name
        self.model = "shellypro1pm"


    def get_point(self):
        if not self.get_all():
            return None
        self.create_point()
        return self.point


    def get_all(self):
        try:
            self.info = self.get_info()
            self.system = self.get_system()
            self.wifi = self.get_wifi()
            self.inputs = self.get_inputs()
            self.switch = self.get_switch()
            self.switch_settings = self.get_switch_settings()
            self.all = {
                'info': self.info,
                'system': self.system,
                'wifi': self.wifi,
                'inputs': self.inputs,
                'switch': self.switch,
                'switch_settings': self.switch_settings
            }
            return True
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error fetching Shelly Pro 1 PM data: {e}")
            return False


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
        return {
            "ip" : self.ip_address,
            "user_defined_name" : self.name,
            "name": data["name"],
            "id": data["id"],
            "mac": data["mac"],
            "slot": data["slot"],
            "model": data["model"],
            "gen": data["gen"],
            "fw_id": data["fw_id"],
            "ver": data["ver"],
            "app": data["app"],
            "auth_en": data["auth_en"],
            "auth_domain": data["auth_domain"]
        }


    def get_system(self):
        '''
        Fetches the system information from the /rpc/Sys.GetStatus endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response data
        '''
        response = requests.get(f"http://{self.ip_address}/rpc/Sys.GetStatus")
        response.raise_for_status()
        data = response.json()
        return {
            "system_mac": data["mac"],
            "system_restart_required": data["restart_required"],
            "system_time": data["time"],
            "system_unixtime": data["unixtime"],
            "system_last_sync_ts": data["last_sync_ts"],
            "system_uptime": data["uptime"],
            "system_ram_size": data["ram_size"],
            "system_ram_free": data["ram_free"],
            "system_ram_min_free": data["ram_min_free"],
            "system_fs_size": data["fs_size"],
            "system_fs_free": data["fs_free"],
            "system_cfg_rev": data["cfg_rev"],
            "system_kvs_rev": data["kvs_rev"],
            "system_schedule_rev": data["schedule_rev"],
            "system_webhook_rev": data["webhook_rev"],
            "system_btrelay_rev": data["btrelay_rev"],
            "system_available_updates": bool(data['available_updates']),
            "system_reset_reason": data["reset_reason"],
            "system_utc_offset": data["utc_offset"]
        }
    
    
    def get_wifi(self):
        '''
        Fetches the WiFi information from the /rpc/WiFi.GetStatus endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response data
        '''
        response = requests.get(f"http://{self.ip_address}/rpc/WiFi.GetStatus")
        response.raise_for_status()
        data = response.json()
        return {
            "wifi_sta_ip" : data["sta_ip"],
            "wifi_status" : data["status"],
            "wifi_ssid" : data["ssid"],
            "wifi_rssi" : data["rssi"],
            "wifi_sta_ip6" : data["sta_ip6"][0]
        }
           

    def get_inputs(self):
        '''
        Fetches the inputs information from the /rpc/Input.GetStatus endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response data
        '''
        inputs = []
        for input_id in [0, 1]:
            response = requests.get(f"http://{self.ip_address}/rpc/Input.GetStatus?id={input_id}")
            response.raise_for_status()
            data = response.json()
            inputs.append(data)

        return {
            "input_0_state" : inputs[0]["state"],
            "input_1_state" : inputs[1]["state"]
        }


    def get_switch(self):
        '''
        Fetches the switch information from the /rpc/Switch.GetStatus endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response data
        '''
        response = requests.get(f"http://{self.ip_address}/rpc/Switch.GetStatus?id=0")
        response.raise_for_status()
        data = response.json()
        
        # Timers
        if "timer_started_at" and "timer_duration" in data:
            data["timer_running"] = self.system["system_unixtime"] - data["timer_started_at"]
            data["timer_remaining"] = data["timer_duration"] - data["timer_running"]
        else:
            data["timer_started_at"] = 0
            data["timer_duration"] = 0
            data["timer_remaining"] = 0
            data["timer_running"] = 0
            
        # Errors
        
        
        errors = ["overvoltage", "undervoltage", "overpower", "overcurrent"]
        for error in errors:
            data[error] = False
            if "errors" in data:
                if error in data["errors"]:
                    data[error] = True
                                
        return {
            "switch_0_source" : data["source"],
            "switch_0_output" : data["output"],
            "switch_0_apower" : data["apower"],
            "switch_0_voltage" : data["voltage"],
            "switch_0_freq" : data["freq"],
            "switch_0_current" : data["current"],
            "switch_0_pf" : data["pf"],
            "switch_0_aenergy_total" : data["aenergy"]["total"],
            "switch_0_aenergy_by_minute_0" : data["aenergy"]["by_minute"][0],
            "switch_0_aenergy_by_minute_1" : data["aenergy"]["by_minute"][1],
            "switch_0_aenergy_by_minute_2" : data["aenergy"]["by_minute"][2],
            "switch_0_aenergy_minute_ts" : data["aenergy"]["minute_ts"],
            "switch_0_ret_aenergy_total" : data["ret_aenergy"]["total"],
            "switch_0_ret_aenergy_by_minute_0" : data["ret_aenergy"]["by_minute"][0],
            "switch_0_ret_aenergy_by_minute_1" : data["ret_aenergy"]["by_minute"][1],
            "switch_0_ret_aenergy_by_minute_2" : data["ret_aenergy"]["by_minute"][2],
            "switch_0_ret_aenergy_minute_ts" : data["ret_aenergy"]["minute_ts"],
            "switch_0_temperature_tC" : data["temperature"]["tC"],
            "switch_0_temperature_tF" : data["temperature"]["tF"],
            "switch_0_timer_started_at" :  int(data["timer_started_at"]),
            "switch_0_timer_duration" :  int(data["timer_duration"]),
            "switch_0_timer_remaining" :  int(data["timer_remaining"]),
            "switch_0_timer_running" : int(data["timer_running"]),
            "switch_0_overvoltage" : data["overvoltage"],
            "switch_0_undervoltage" : data["overvoltage"],
            "switch_0_overvoltage" : data["overvoltage"],
            "switch_0_overvoltage" : data["overvoltage"]
        }
        
        
    def get_switch_settings(self):
        '''
        Fetches the switch settings from the /rpc/Switch.GetConfig endpoint.
        
        Args:
           None

        Returns:
            dict: The JSON response data
        '''
        response = requests.get(f"http://{self.ip_address}/rpc/Switch.GetConfig?id=0")
        response.raise_for_status()
        data = response.json()      
        return {
            "switch_0_name": data["name"],
            "switch_0_in_mode": data["in_mode"],
            "switch_0_in_locked": data["in_locked"],
            "switch_0_initial_state": data["initial_state"],
            "switch_0_auto_on": data["auto_on"],
            "switch_0_auto_on_delay": data["auto_on_delay"],
            "switch_0_auto_off": data["auto_off"],
            "switch_0_auto_off_delay":data["auto_off_delay"],
            "switch_0_power_limit": data["power_limit"],
            "switch_0_voltage_limit": data["voltage_limit"],
            "switch_0_undervoltage_limit": data["undervoltage_limit"],
            "switch_0_autorecover_voltage_errors": data["autorecover_voltage_errors"],
            "switch_0_current_limit": data["current_limit"],
            "switch_0_reverse": data["reverse"],
            "switch_0_input_id": data["input_id"]
        }
        
        
    def create_point(self):
        '''
        Constructs a dictionary in the InfluxDB Flux point structure\n
        stored in self.point
        
        Args:
           None

        Returns:
            None
        '''
        self.point =  {
            "measurement": "shellypro1pm",
            "tags": {
                **self.info
            },
            "fields": {
                **self.system,
                **self.wifi,
                **self.inputs,
                **self.switch,
                **self.switch_settings
            }
        }
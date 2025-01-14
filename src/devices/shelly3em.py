import requests




class Shelly3EM:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_status(self):
        url = f"http://{self.ip_address}/status"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_emeter_data(self, emeter_index=0):
        status = self.get_status()
        return status['emeters'][emeter_index]

    def format_data_to_influx(self, info, data):
        points = []
        common_tags = {
            "type": info["type"],
            "mac": info["mac"],
            "fw": info["fw"],
            "ip": data["wifi_sta"]["ip"]
        }

        # Process relays
        for index, relay in enumerate(data["relays"]):
            point = {
                "measurement": "shelly3em",
                "tags": {
                    **common_tags,
                    "component": "relay",
                    "index": index
                },
                "fields": {
                    **relay
                }
            }
            points.append(point)

        # Process emeters
        for index, emeter in enumerate(data['emeters']):
            point = {
                "measurement": "shelly3em",
                "tags": {
                    **common_tags,
                    "component": "emeter",
                    "index": index
                },
                "fields": {
                    **emeter
                }
            }
            points.append(point)

        # Process the n emeter
        point = {
            "measurement": "shelly3em",
            "tags": {
                **common_tags,
                "component": "emeter_n"
            },
            "fields": {
                **data["emeter_n"]
            }
        }
        points.append(point)

        # Process common components
        point = {
            "measurement": "shelly3em",
            "tags": {
                **common_tags,
                "component": "common"
            },
            "fields": {
                "total_power": data['total_power'],
                "ram_total": data['ram_total'],
                "ram_free": data['ram_free'],
                "uptime": data['uptime']
            }
        }
        points.append(point)

        # Process WiFi stats
        point = {
            "measurement": "shelly3em",
            "tags": {
                **common_tags,
                "component": "wifi"
            },
            "fields": {
                **data["wifi_sta"]
            }
        }
        points.append(point)

        return points

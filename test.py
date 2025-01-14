import requests
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os
import time

def get_devices(file_path):
    """
    Reads the devices list from a JSON file.
    
    Args:
        file_path (str): The path to the devices.json file.

    Returns:
        list: A list of devices with their IPs and models.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def get_shelly_info(base_url):
    """
    Fetches the basic information from the /shelly endpoint.
    
    Args:
        base_url (str): The base URL of the Shelly device (e.g., http://192.168.1.100).

    Returns:
        dict: The JSON response from the /shelly endpoint.
    """
    try:
        response = requests.get(f"{base_url}/shelly")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Shelly info: {e}")
        return None

def get_meter_status(base_url):
    """
    Fetches the meter statuses from the /status endpoint.
    
    Args:
        base_url (str): The base URL of the Shelly device (e.g., http://192.168.1.100).

    Returns:
        dict: The JSON response from the /status endpoint.
    """
    try:
        response = requests.get(f"{base_url}/status")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching meter status: {e}")
        return None

def get_influx_settings():
    """
    Loads InfluxDB connection settings from a .env file.

    Returns:
        dict: A dictionary containing InfluxDB settings.
    """
    load_dotenv()
    return {
        "url": os.getenv("INFLUXDB_URL"),
        "token": os.getenv("INFLUXDB_TOKEN"),
        "org": os.getenv("INFLUXDB_ORG"),
        "bucket": os.getenv("INFLUXDB_BUCKET")
    }

def format_data_to_influx(info, data, model):
    """
    Formats Shelly data into InfluxDB point format.

    Args:
        info (dict): The info to format.
        data (dict): The data to format.
        model (str): The model of the Shell device.

    Returns:
        list: A list of InfluxDB Point objects.
    """
    # Blank points list to append points 
    points = []
    
    # Common tags for all points
    common_tags = {
        "type": info["type"],
        "mac": info["mac"],
        "fw" : info["fw"],
        "ip" : data["wifi_sta"]["ip"]
    }
    
    #################################
    # Process the "shelly3em" model #
    #################################
    if model == "shelly3em":
        # Process relays
        for index, relay in enumerate(data["relays"]):
            point = {
                "measurement": model,
                "tags": {
                    **common_tags,
                    "component" : "relay",
                    "index" : index
                    
                },
                "fields": {
                    **relay
                }
            }
            points.append(point)
        
        # Process emeters
        for index, emeter in enumerate(data['emeters']):
            point = {
                "measurement": model,
                "tags": {
                    **common_tags,
                    "component" : "emeter",
                    "index" : index
                },
                "fields": {
                    **emeter
                }
            }
            points.append(point)
            
        # Process the n emeter
        point = {
            "measurement": model,
            "tags": {
                **common_tags,
                "component" : "emeter_n"
            },
            "fields": {
                **data["emeter_n"]
            }
        }
        points.append(point)

        # Process common components
        point = {
            "measurement": model,
            "tags": {
                **common_tags,
                "component" : "common"
            },
            "fields": {
                "total_power" : data['total_power'],
                "ram_total" : data['ram_total'],
                "ram_free" : data['ram_free'],
                "uptime" : data['uptime']
            }
        }
        points.append(point)
        
        # Process WiFi stats
        point = {
            "measurement": model,
            "tags": {
                **common_tags,
                "component" : "wifi"
            },
            "fields": {
                **data["wifi_sta"]
            }
        }
        points.append(point)
        
    return points
            

def upload_to_influx(influx_settings, points):
    """
    Uploads data to an InfluxDB v2 server.

    Args:
        influx_settings (dict): The InfluxDB connection settings.
        points (list): The points data to upload.
    """
    # try:
    with InfluxDBClient(url=influx_settings["url"], token=influx_settings["token"], org=influx_settings["org"]) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=influx_settings["bucket"], record=points)
        print(f"Wrote {len(points)} points to InfluxDB.")
    # except Exception as e:
    #     print(f"Error uploading to InfluxDB: {e}")


def main():
    # Path to the devices.json file
    devices_file = "devices.json"

    print("Fetching devices from devices.json...")
    devices = get_devices(devices_file)

    if not devices:
        print("No devices found. Exiting.")
        return

    influx_settings = get_influx_settings()

    while True:
        for device in devices:
            ip = device.get("ip")
            model = device.get("model")
            if not ip:
                print(f"Skipping device with missing IP: {device}")
                continue

            print(f"Processing device {model} at {ip}...")
            base_url = f"http://{ip}"

            print("Fetching Shelly basic info...")
            shelly_info = get_shelly_info(base_url)

            print("Fetching meter statuses...")
            meter_status = get_meter_status(base_url)
            if meter_status and shelly_info:
                points = format_data_to_influx(shelly_info, meter_status, device.get("model"))
        
        print(points)
        upload_to_influx(influx_settings, points)
        
        print("Sleeping for 10 seconds...")
        time.sleep(10)

if __name__ == "__main__":
    main()
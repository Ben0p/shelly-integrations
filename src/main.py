import requests
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os
import time
# Device classes
from devices.shelly3em import Shelly3EM
from devices.shellypro1pm import ShellyPro1Pm




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
    '''
    Fetches the basic information from the /shelly endpoint.
    
    Args:
        base_url (str): The base URL of the Shelly device (e.g., http://192.168.1.100).

    Returns:
        dict: The JSON response from the /shelly endpoint.
    '''
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
        shelly_device = Shelly3EM(info["ip"])
        points = shelly_device.format_data_to_influx(info, data)
        
    return points
            

def upload_to_influx(influx_settings, points):
    """
    Uploads data to an InfluxDB v2 server.

    Args:
        influx_settings (dict): The InfluxDB connection settings.
        points (list): The points data to upload.
    """
    try:
        with InfluxDBClient(url=influx_settings["url"], token=influx_settings["token"], org=influx_settings["org"], verify_ssl=False) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=influx_settings["bucket"], record=points)
            print(f"Wrote {len(points)} points to InfluxDB.")
    except Exception as e:
        print(f"Error uploading to InfluxDB: {e}")


def main():
    # TODO: Update to proper logging service
    # TODO: Update environment loading service
    load_dotenv()
    devices_file = os.getenv("JSON_FILE", "devices.json")
    if not devices_file:
        print("Error: JSON_FILE environment variable not set.")
        return

    print("Fetching devices from devices.json...")
    devices = get_devices(devices_file)

    if not devices:
        print("No devices found. Exiting.")
        return

    influx_settings = get_influx_settings()

    # Initialize InfluxDB client
    # TODO: Make the influx connection and methods a class
    influx_client = InfluxDBClient(url=influx_settings["url"], token=influx_settings["token"], org=influx_settings["org"])
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    while True:
        all_points = []
        for device in devices:
            # TODO: Initialize classes of each device once then do the get_point() method periodically
            
            ###############
            # Shelly 3 EM #
            ###############
            # TODO: Self contain the shelly 3 em class the same as shelly pro 1 pm
            if device["model"] == "shelly3em":
                device_class = Shelly3EM(device["ip"])

                print(f"Processing shelly3em at {device_class.ip_address}...")

                print("Fetching Shelly basic info...")
                shelly_info = get_shelly_info(f"http://{device_class.ip_address}")

                print("Fetching meter statuses...")
                meter_status = device_class.get_status()
                if meter_status and shelly_info:
                    points = device_class.format_data_to_influx(shelly_info, meter_status)
                    all_points.extend(points)

            ###################
            # Shelly Pro 1 PM #
            ###################               
            elif device["model"] == "shellypro1pm":
                device_class = ShellyPro1Pm(device["ip"], device["name"])
                point = device_class.get_point()
                if point:
                    all_points.append(point)
                
        # Upload all points to InfluxDB
        if all_points:
            try:
                write_api.write(bucket=influx_settings["bucket"], record=all_points)
                print(f"Wrote {len(all_points)} points to InfluxDB.")
            except Exception as e:
                print(f"Error uploading to InfluxDB: {e}")

        print("Sleeping for 10 seconds...")
        time.sleep(10)


if __name__ == "__main__":
    main()

import requests
import json


def get_results(ip):
    # get status
    url = "http://" + ip + ":8008/setup/bluetooth/status"
    response = requests.request("GET", url)

    # if we're not scanning, start scanning
    if not response.json()['scanning_enabled']:
        start_scan(ip)

    url = "http://" + ip + ":8008/setup/bluetooth/scan_results"

    response = requests.request("GET", url)

    response_json = response.json()

    devices = {dev['mac_address']: dev['rssi'] for dev in response_json}

    print("scan results of", ip, ":", devices)

    return devices


def get_device_info(ip):
    url = "http://" + ip + ":8008/setup/eureka_info"

    querystring = {"params": "name"}

    response = requests.request("GET", url, params=querystring)

    return (response.json()['name'])


def start_scan(ip):
    print("scanning on " + ip)
    # starts scan
    url = "http://" + ip + ":8008/setup/bluetooth/scan"

    payload = json.dumps({"enable": True, "clear_results": True, "timeout": 60})

    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.ok)

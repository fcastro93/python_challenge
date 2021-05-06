import sys
import urllib
import requests


def get_geo_bulk(ips):
    bulk_flag = True
    url = "https://app.ipapi.co/bulk/"

    payload = f'q={ips}&output=json'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__cfduid=dbfa8012b0211e69dbf5a9084eddb2f781620267441; csrftoken=kMHwN0itsk4tiySG2KI903wGqkcyGAdWCRFWTxPa1SMZibgoTuOPyaRhbdX0RDjF'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    msg = response_json.get("msg", False)
    if msg != False:
        print("Key for bulk expired because free version got it limit, switching to individual request")
        bulk_flag = False
    return response.json(), bulk_flag


def get_geo_individual(ip):
    url = "https://freegeoip.app/json/{}".format(ip)
    headers = {
        'accept': "application/json",
        'content-type': "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()


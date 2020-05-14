import requests
import urllib3
from pprint import pprint
import json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("PATH/TO/creds.json") as credentials:
    creds = json.load(credentials)

# Initialized Netbox token and headers for connection
netbox_token = 'Token GOES HERE'
headers = {
    'Accept': 'application/json',
    'Authorization': f'{netbox_token}',
    'Content-Type': 'application/json'
           }


sw_info = swis.query("SELECT Address, CIDR, Comments, VLAN, Location FROM IPAM.Subnet")


def create_prefix():

    vlan_result = requests.get("https://NETBOX-SERVER/api/ipam/vlans/",
                                 headers=headers, verify=False)
    all_vlans = []

    vlan_payload = vlan_result.json()
    all_vlans.append(vlan_payload)

    while vlan_payload['next'] is not None:
        response = requests.get(vlan_payload['next'],
                                headers=headers, verify=False)
        vlan_payload = response.json()
        all_vlans.append(vlan_payload)

    vlan_list = []
    for entry in all_vlans:
        info = entry['results']


        for vlan in info:
            vlan_dict = {}

            vlan_dict['tag'] = vlan['vid']
            vlan_dict['name'] = vlan['name']
            vlan_dict['id'] = vlan['id']

            vlan_list.append(vlan_dict)
    #pprint(vlan_list)

    sw_list = []
    for sw_entry in sw_info:
        sw_dict = {}
        #sw_dict['address'] = sw_entry['Address']
        sw_address = sw_entry['Address']

        sw_cidr = sw_entry['CIDR']
        sw_dict['vlan'] = sw_entry['VLAN']

        sw_comments = sw_entry['Comments']
        sw_dict['name'] = sw_entry['Comments']

        #sw_list.append(sw_address)
        sw_prefix = f'{sw_address}/{sw_cidr}'
        sw_dict['prefix'] = sw_prefix
        sw_list.append(sw_dict)

        #pprint(sw_dict)

    print("Checking for duplicates now")
    prefix_result = requests.get("https://NETBOX-SERVER/api/ipam/prefixes/",
                                 headers=headers, verify=False)
    all_prefixes = []

    prefix_payload = prefix_result.json()
    all_prefixes.append(prefix_payload)

    while prefix_payload['next'] is not None:
        response = requests.get(prefix_payload['next'],
                                headers=headers, verify=False)
        prefix_payload = response.json()
        all_prefixes.append(prefix_payload)

    nb_list = []
    for nb_entry in all_prefixes:
        results = nb_entry['results']


        for entry in results:
            nb_prefix = entry['prefix']
            nb_list.append(nb_prefix)

    for entry in sw_list:
        if entry['prefix'] not in nb_list:
            if entry['name'] is not None:

                prefix = {
                    "prefix": f"{entry['prefix']}",
                    "status": 1,
                    "description": f"{entry['name']}"
                }

                result = requests.post("https://NETBOX-SERVER/api/ipam/prefixes/",
                                   headers=headers, verify=False, data=json.dumps(prefix))
                pprint(result)


def prefix_name():
    prefix_result = requests.get("https://NETBOX-SERVER/api/ipam/prefixes/",
                                 headers=headers, verify=False)
    all_prefixes = []

    prefix_payload = prefix_result.json()
    all_prefixes.append(prefix_payload)

    while prefix_payload['next'] is not None:
        response = requests.get(prefix_payload['next'],
                                headers=headers, verify=False)
        prefix_payload = response.json()
        all_prefixes.append(prefix_payload)

    for entry in all_prefixes:
        results = entry['results']

        for nb_entry in results:
            nb_prefix = nb_entry['prefix']
            nb_desc = nb_entry['description']
            nb_prefix_id = nb_entry['id']

            if nb_desc == "":
                for sw_entry in sw_info:
                    sw_address = sw_entry['Address']
                    sw_cidr = sw_entry['CIDR']
                    sw_comments = sw_entry['Comments']
                    sw_prefix = f'{sw_address}/{sw_cidr}'

                    if sw_comments is not None and sw_comments is not "":

                        if nb_prefix in sw_prefix:
                            if sw_comments is not None or sw_comments is not "":
                                update_data = {
                                    "description": f"{sw_comments}"
                                }
                                prefix_update_result = requests.patch(
                                    f"https://NETBOX-SERVER/api/ipam/prefixes/{nb_prefix_id}/",
                                                            headers=headers, verify=False, data=json.dumps(update_data))
                                pprint(prefix_update_result)

def main():

    user_choice = input('''
(1) Create prefix using data from SolarWinds IPAM
(2) Update prefix names    
    ''')

    if "1" in user_choice.lower() or "create" in user_choice.lower():
        create_prefix()

    elif "2" in user_choice.lower() or "name" in user_choice.lower():
        prefix_name()


if __name__ == "__main__":
    main()
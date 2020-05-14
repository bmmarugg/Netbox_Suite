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

response = requests.get("https://NETBOX-SEVER-HERE/api/dcim/sites/",
                     headers=headers, verify=False)

info = response.json()

site_info = info['results']

for entry in site_info:
    site_name = entry['name']
    site_id = entry['id']


def main():
    vlan_result = requests.get("https://NETBOX-SEVER-HERE/api/ipam/vlans/",
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

            nb_vlan = vlan['vid']
            nb_name = vlan['name']
            nb_id = vlan['id']
            nb_site = vlan['site']

            if nb_site is None:
                for sw_entry in sw_info:
                    sw_address = sw_entry['Address']
                    sw_cidr = sw_entry['CIDR']
                    sw_comments = sw_entry['Comments']
                    sw_prefix = f'{sw_address}/{sw_cidr}'
                    sw_site = sw_entry['Location']
                    sw_vlan = sw_entry['VLAN']

                    if str(nb_vlan) in str(sw_vlan):
                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

                        if "SITE-NAME" in sw_site.lower():
                            site = {
                                "site": "SITE-ID"
                            }

                            site_result = requests.patch(f"https://NETBOX-SEVER-HERE/api/ipam/vlans/{nb_id}/",
                                                         headers=headers, verify=False, data=json.dumps(site))

                            pprint(site_result)

if __name__ == "__main__":
    main()


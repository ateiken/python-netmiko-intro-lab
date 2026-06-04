import pynetbox
from netmiko import ConnectHandler
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import json

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()

for device in devices:
    if not device.primary_ip:
        continue
    ip = str(device.primary_ip).split('/')[0]

    try:
        conn = ConnectHandler(
            device_type='arista_eos',
            host=ip,
            username='ansible',
            password='automation',
        )

        output = conn.send_command('show ip bgp summary | json')
        bgp_data = json.loads(output)
        
        peers = bgp_data['vrfs']['default']['peers']
        print(f"\n{device.name} BGP Summary:")
        print(f"  {'Neighbor':<20} {'AS':<10} {'State':<15}")
        print(f"  {'-'*45}")
        for neighbor, data in peers.items():
            print(f" {neighbor:<20} {data['asn']:<10} {data['peerState']:<15}")
        
        conn.disconnect()
        
        

    except NetmikoTimeoutException:
        print(f'{device.name}: Connection timed out')
    except NetmikoAuthenticationException:
        print(f'{device.name}: Authentication failed')
    except Exception as e:
        print(f'{device.name}: An error occurred - {str(e)}')
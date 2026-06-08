import pynetbox
from netmiko import ConnectHandler
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import json

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()

for device in devices:
    if not device.primary_ip:
        continue
        # only push to leafs
    if device.role.slug != 'leaf-switch':
        continue
    
    ip = str(device.primary_ip).split('/')[0]

    try:
        conn = ConnectHandler(
            device_type='arista_eos',
            host=ip,
            username='ansible',
            password='automation',
        )

        # define config to push
        config_commands = [
            'banner motd',
            'Managed by Netmiko',
            'EOF'
        ]
        
        output = conn.send_config_set(config_commands)
        print(f'{device.name}: Configuration applied successfully')
        print(output)
        
        conn.disconnect()
        
        

    except NetmikoTimeoutException:
        print(f'{device.name}: Connection timed out')
    except NetmikoAuthenticationException:
        print(f'{device.name}: Authentication failed')
    except Exception as e:
        print(f'{device.name}: An error occurred - {str(e)}')
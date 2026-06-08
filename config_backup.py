import pynetbox
from netmiko import ConnectHandler
from datetime import datetime
import os

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')
devices = list(nb.dcim.devices.all())

# create backup directory with timestamp
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_dir = f'backups/{timestamp}'
os.makedirs(backup_dir, exist_ok=True)
print(f'saving backups to {backup_dir}')

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
        
        output = conn.send_command('show running-config')
        
        filename = f'{backup_dir}/{device.name}.cfg'
        with open(filename, 'w') as f:
            f.write(f'! Backup of {device.name}\n')
            f.write(output)

        print(f'{device.name}: saved to {filename}')
        conn.disconnect()
        
        
    except NetmikoTimeoutException:
        print(f'{device.name}: Connection timed out')
    except NetmikoAuthenticationException:
        print(f'{device.name}: Authentication failed')
    except Exception as e:
        print(f'{device.name}: An error occurred - {str(e)}')
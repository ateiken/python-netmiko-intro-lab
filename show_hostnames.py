import pynetbox
from netmiko import ConnectHandler

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()

for device in devices:
    if not device.primary_ip:
        continue
    ip = str(device.primary_ip).split('/')[0]

    conn = ConnectHandler(
        device_type='arista_eos',
        host=ip,
        username='ansible',
        password='automation',
    )

    output = conn.send_command('show hostname')
    print(f'{device.name}: {output.strip()}')
    conn.disconnect()

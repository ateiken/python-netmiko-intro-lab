import pynetbox
from netmiko import ConnectHandler
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()

required_config = [
            'ip routing',
            'ip routing vrf CUST_ACME',
            'ip routing vrf CUST_GLOBEX',
        ]

prohibited_config = [
            'telnet',
        ]

for device in devices:
    if not device.primary_ip:
        continue
    
    ip = str(device.primary_ip).split('/')[0]
    issues = []

    try:
        conn = ConnectHandler(
            device_type='arista_eos',
            host=ip,
            username='ansible',
            password='automation',
        )
        
        output = conn.send_command('show running-config')
        conn.disconnect()
        
        for check in required_config:
            if check not in output:
                issues.append(f'Missing required config: {check}')
        for check in prohibited_config:
            if check in output:
                issues.append(f'Prohibited config found: {check}')
        print(f"{'device':<20} {'status':<10} {'Issues'}")
        print('-' * 60)
        
        if issues:
            print(f'{device.name:<20} {"FAIL":<10} {", ".join(issues)}')
        else:
            print(f'{device.name:<20} {"PASS":<10}')

    except NetmikoTimeoutException:
        print(f'{device.name}: Connection timed out')
    except NetmikoAuthenticationException:
        print(f'{device.name}: Authentication failed')
    except Exception as e:
        print(f'{device.name}: An error occurred - {str(e)}')
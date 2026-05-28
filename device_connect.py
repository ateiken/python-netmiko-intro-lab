from netmiko import ConnectHandler

# define device connection params
device = {
    'device_type': 'arista_eos',
    'host': '192.168.8.101',
    'username': 'ansible',
    'password': 'automation',
}

# connect to device
connection = ConnectHandler(**device)

# run a command
output = connection.send_command('show version')
print(output)

connection.disconnect()
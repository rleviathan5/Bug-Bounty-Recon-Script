import subprocess
import os

def check_for_tools_linux():
    path = '/usr/bin/'
    if os.path.exists(path + 'nmap'):
        print('Nmap exists')
    else:
        print('nope')

    if os.path.exists(path + 'gospider'):
        print('Gospider exists')
    else:
        print('nope')

    if os.path.exists(path + 'gobuster'):
        print('Gobuster exists')
    else:
        print('nope')

nmap_command = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
gospider_command = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
gobuster_command = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

#print(nmap_command.stdout)
import subprocess
import shutil
import re

def check_for_tools():
    tools = ['nmap', 'gospider', 'gobuster']

    for tool in tools:
        if shutil.which(tool):
            print(f"{tool} exists")
        else:
            print(f"{tool} missing")

def check_valid_ipv4(ipv4_input):
    ipv4_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
    match = re.search(ipv4_pattern, ipv4_input)

    if match:
        print("true")
        return
    else:
        ipv4_retry = input("Please enter a valid Ipv4 address")
        check_valid_ipv4(ipv4_retry)



#main body

check_for_tools()
ipv4_input = input("Enter Ipv4 address to scan")
check_valid_ipv4(ipv4_input)



nmap_command = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
#gospider_command = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
gobuster_command = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

#print(nmap_command.stdout)


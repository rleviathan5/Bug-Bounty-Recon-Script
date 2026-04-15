import subprocess
import os
import shutil

def check_for_tools():
    tools = ['nmap', 'gospider', 'gobuster']

    for tool in tools:
        if shutil.which(tool):
            print(f"{tool} exists")
        else:
            print(f"{tool} missing")


check_for_tools()
nmap_command = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
gospider_command = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
gobuster_command = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

#print(nmap_command.stdout)
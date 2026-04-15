import subprocess

nmap_command = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
gospider_command = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
gobuster_command = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

print(nmap_command.stdout)
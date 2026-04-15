import subprocess

nmap_command = subprocess.run(['nmap', '-h'], capture_output=True, text=True)

print(nmap_command.stdout)
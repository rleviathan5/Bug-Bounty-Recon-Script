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
    ipv4_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}' ## https://ihateregex.io/expr/ip/
    match = re.search(ipv4_pattern, ipv4_input)

    if match:
        return
    else:
        ipv4_retry = input("Please enter a valid Ipv4 address: ")
        check_valid_ipv4(ipv4_retry)

def display_tool_help_menu(help_menu_input):
    if help_menu_input == "y" or help_menu_input == "Y":
        nmap_h = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
        gospider_h = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
        gobuster_h = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

        print(nmap_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n") #seperating the help menus
        print(gospider_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
        print(gobuster_h.stdout)
    elif help_menu_input == "n" or help_menu_input == "N":
        return
    else:
        help_menu_input_retry = input("Display Tool Help Menus? (y/n): ")
        display_tool_help_menu(help_menu_input_retry)

#main body
check_for_tools()

print("Simple Bug Bounty Hunting Recon Tool\n\n")
help_menu_input = input("Display Tool Help Menus? (y/n): ")
display_tool_help_menu(help_menu_input)

ipv4_input = input("\n\n\nEnter Ipv4 address to scan: ")
check_valid_ipv4(ipv4_input)






import subprocess
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, wait
import argparse

def check_for_tools():
    tools = ['nmap', 'gospider', 'gobuster']
    results = []

    for tool in tools:
        if shutil.which(tool):
            results.append(f"{tool} exists")
        else:
            results.append(f"{tool} missing")

    print(" | ".join(results)) #seperating print statements with a pipe symbol

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

def test_flag_gospider():
    pattern = r".*\.(png|jpg|jpeg|gif|svg|ico|css|woff|woff2|ttf|map)$" #unorthodox flags are to stop massive asset explosion due to juice-shop being a single page app
    return subprocess.run(                                              
        ['gospider', '-s', 'http://juice-shop.local:3000', 
         '-d', '1', '-c', '2', '-t', '4', '-q', '--js=false', 
         '--blacklist', pattern, '--output', 'gospider-output'],
         capture_output=True, 
         text=True
         )
    
def test_flag_gobuster():
    return subprocess.run(
        ['gobuster', 'dir', '-u', 'http://juice-shop.local:3000', 
         '-w', 'common.txt', '-t', '5', '--exclude-length', '75002', '-o', 'gobuster.txt'],
         capture_output=True, 
         text=True
         )

def test_flag_nmap():
    return subprocess.run(
        ['nmap', '-sV', '-sS', '-p', '3000', '-oN', 'nmap.txt', 'juice-shop.local'],
        capture_output=True,
        text=True
    )
    
def display_script_help_menu():
    print("\nThis simple Bug Bounty Hunting script uses nmap, gospider and gobuster")
    print("https://nmap.org/docs.html | https://github.com/jaeles-project/gospider | https://github.com/Oj/gobuster")
    print("\nFLAGS:")
    print("\t--help: Display help menu for recon.py script")
    print("\t--tools: Display help menus for packaged recon tools")
    print("\t--test: Test recon tools against local OWASP Juice Shop (see README)")
    print("\t--domain {Valid Domain}: Specify a target for all recon tools")
    print("\nRECON TOOL DEFAULT FLAGS")
    print("\tnmap -sV -sS -oN nmap.txt {target domain}")
    print("\tgospider -s {target domain} -d 1 -c 2 -t 4 -q --output gospider-output")
    print("\tgobuster gobuster dir -u {target domain} -w common.txt -t 5 -o gobuster.txt")

def add_argparse_fields():
    parser = argparse.ArgumentParser(description="Simple Bug Bounty Hunting Recon Tool")
    parser.add_argument("--tools", required=False, help="Display help menus for packaged recon tools")

    args = parser.parse_args()



def main():
    check_for_tools()
    add_argparse_fields()
    
    print("\nThreads starting")
    with ThreadPoolExecutor(max_workers=2) as executor:  
        threads = [
            executor.submit(test_flag_gospider),
            executor.submit(test_flag_gobuster),
            executor.submit(test_flag_nmap)
            ]
        print("Crawling...")
        wait(threads) #block until all threads are done
    print("Threads finished")

main()







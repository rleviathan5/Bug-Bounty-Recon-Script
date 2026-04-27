import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import shlex
from shodan import Shodan
import socket
import json

def add_argparse_fields():
    parser = argparse.ArgumentParser(description="Simple Bug Bounty Hunting Recon Tool")
    parser.add_argument("--tools", action="store_true", required=False, help="Display help menus for packaged recon tools")
    parser.add_argument("--test", action="store_true", required=False, help="Test recon tools against local OWASP Juice Shop (see README)")
    parser.add_argument("--domain", metavar="{target}", required=False, help="Specify a target for all recon tools")
    parser.add_argument("--port", metavar="{target port}", type=int, required=False, help="Specify a specific port for all recon tools")
    parser.add_argument("--custom", action="store_true", required=False, help="Reads commands from 'input/commands.txt' and executes them in parallel")
    parser.add_argument("--shodan", metavar="{target}", required=False, help="Query Shodan api against a target")
    
    return parser.parse_args()
  
def preprocess_custom_flag(commands):
    #to prevent user from executing unintended commands
    #evil command gets prepended with nmap/gospider/gobuster so it will fail
    #valid commands will function as normal
    result = []
    for cmd in commands:
        if not re.search(r'\bnmap\s+', cmd):
            cmd = re.sub(r'(-[su]\s+)(?!https?://)(\S+)', r'\1http://\2', cmd)

        cmd = re.sub(r'\b(?:nmap|gospider|gobuster)\s+', '', cmd).strip()
        result.append(cmd)
    return result
    
def split_json_cves(data):
    #modifying the returned json in place
    #delete the cve info from original and append it to a new array
    cves = []

    for service in data.get('data', []):
        if 'vulns' in service:
            cves.append(service['vulns'])
            del service['vulns']

    return data, cves

def tools_flag():
    try:
        nmap_h = subprocess.run(['nmap', '-h'], capture_output=True, text=True, check=True)
        gospider_h = subprocess.run(['gospider', '-h'], capture_output=True, text=True, check=True)
        gobuster_h = subprocess.run(['gobuster', '-h'], capture_output=True, text=True, check=True)
    except Exception as e:
        print(e)

    print(nmap_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n") #seperating the help menus
    print(gospider_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    print(gobuster_h.stdout)

def test_flag(port):
    nmap_cmd = 'nmap -sV -sS -oN output/nmap.txt juice-shop.local'
    gospider_cmd = 'gospider -s http://juice-shop.local -d 1 -c 2 -t 4 -q --js=false --output output/gospider-output' #--js=false to stop massive asset explosion when crawling juice-shop
    gobuster_cmd = 'gobuster dir -u http://juice-shop.local -w input/common.txt -t 5 --exclude-length 75002 -o output/gobuster.txt' #--exclude-length 75002 juice-shop specific setting

    if port is not None:
        nmap_cmd + '-p ' + str(port) #append '-p {port}' to nmap command
        gospider_cmd = re.sub(r'(-[su]\s+)(\S+)', rf'\1\2:{port}', gospider_cmd) #find either the '-s' or '-u' switch, go to the end of the next string and append ':{port}'
        gobuster_cmd = re.sub(r'(-[su]\s+)(\S+)', rf'\1\2:{port}', gobuster_cmd)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        threads = [
            executor.submit(lambda: subprocess.run(shlex.split(nmap_cmd), capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(shlex.split(gospider_cmd), capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(shlex.split(gobuster_cmd), capture_output=True, text=True, check=True))
        ]

        print("Crawling...")

        for thread in as_completed(threads): #throw errors as soon as they occur
            try:
                thread.result() #block until all threads are done
            except Exception as e:
                print(e)

        print("Done")

def domain_flag(input_domain, port):
    nmap_cmd = 'nmap -sV -sS -T3 -oN output/nmap.txt ' + input_domain
    gospider_cmd = 'gospider -s ' + input_domain + ' -d 1 -c 2 -t 2 -q --output output/gospider-output'
    gobuster_cmd = 'gobuster dir -u ' + input_domain + ' -w input/common.txt -t 1 -o output/gobuster.txt'

    nmap_cmd = re.sub(r'https?://', '', nmap_cmd) #removing http(s):// from nmap command, gospider and gobuster need the http(s)

    if port is not None:
        nmap_cmd + '-p ' + str(port) #append '-p {port}' to nmap command
        gospider_cmd = re.sub(r'(-[su]\s+)(\S+)', rf'\1\2:{port}', gospider_cmd) #find either the '-s' or '-u' switch, go to the end of the next string and append ':{port}'
        gobuster_cmd = re.sub(r'(-[su]\s+)(\S+)', rf'\1\2:{port}', gobuster_cmd)

    with ThreadPoolExecutor(max_workers=3) as executor:  
        threads = [
            executor.submit(lambda: subprocess.run(shlex.split(nmap_cmd), capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(shlex.split(gospider_cmd), capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(shlex.split(gobuster_cmd), capture_output=True, text=True, check=True))
        ]

        print("Crawling...")

        for thread in as_completed(threads): #throw errors as soon as they occur
            try:
                thread.result() #block until all threads are done
            except Exception as e:
                print(e)

        print("Done")

def custom_flag():
    with open("input/commands.txt", "r") as file:
        commands = [line.strip() for line in file]
        processed_commands = preprocess_custom_flag(commands)

    with ThreadPoolExecutor(max_workers=3) as executor:  
        threads = [
            executor.submit(lambda: subprocess.run(['nmap'] + shlex.split(processed_commands[0]) + ['-oN', 'output/nmap.txt'], capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(['gospider'] + shlex.split(processed_commands[1]) + ['--output', 'output/gospider-output'], capture_output=True, text=True, check=True)),
            executor.submit(lambda: subprocess.run(['gobuster'] + shlex.split(processed_commands[2]) + ['-o', 'output/gobuster.txt'], capture_output=True, text=True, check=True))
            ]
        
        print("Crawling...")

        for thread in as_completed(threads): #throw errors as soon as they occur
            try:
                thread.result() #block until all threads are done
            except Exception as e:
                print(e)

        print("Done")

def shodan_flag(input_domain):
    with open('input/apikey.txt', 'r') as file:
        key = file.readline().strip() 
        api = Shodan(key)
    
    try:
        target_ip = socket.gethostbyname(input_domain) #free shodan api doesnt allow domain lookups, so need to resolve domain to an ip before parsing to shodan
        target_info = api.host(target_ip)
    except Exception as e:
        print(e)
    
    clean_json, cve_json = split_json_cves(target_info)

    with open('output/shodan_clean.json', 'w') as file:
        json.dump(clean_json, file, indent=4)

    with open('output/shodan_cves.json', 'w') as file:
        json.dump(cve_json, file, indent=4)

def main():
    args = add_argparse_fields()

    if args.test: test_flag(args.port)
    if args.tools: tools_flag()
    if args.domain: domain_flag(args.domain, args.port) #pass input to function
    if args.custom: custom_flag()
    if args.shodan: shodan_flag(args.shodan)
    
main()

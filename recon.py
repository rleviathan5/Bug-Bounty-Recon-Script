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

def preprocess_command(commands):
    result = []
    for cmd in commands:
        if not re.search(r'\bnmap\s+', cmd):
            cmd = re.sub(r'(-[su]\s+)(?!https?://)(\S+)', r'\1http://\2', cmd)

        cmd = re.sub(r'\b(?:nmap|gospider|gobuster)\s+', '', cmd).strip()
        result.append(cmd)
    return result
    
def tools_flag():
    nmap_h = subprocess.run(['nmap', '-h'], capture_output=True, text=True)
    gospider_h = subprocess.run(['gospider', '-h'], capture_output=True, text=True)
    gobuster_h = subprocess.run(['gobuster', '-h'], capture_output=True, text=True)

    print(nmap_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n") #seperating the help menus
    print(gospider_h.stdout, "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    print(gobuster_h.stdout)
    

    return subprocess.run(
        ['nmap', '-sV', '-sS', '-p', '3000', '-oN', 'nmap.txt', 'juice-shop.local'],
        capture_output=True,
        text=True
    )

def test_flag():
    with ThreadPoolExecutor(max_workers=3) as executor:  
        threads = [
            executor.submit(lambda: subprocess.run(
                ['nmap', '-sV', '-sS', '-p', '3000', '-oN', 'nmap.txt', 'juice-shop.local'],
                capture_output=True, text=True
        )),
            executor.submit(lambda: subprocess.run(                                              
                ['gospider', '-s', 'http://juice-shop.local:3000', 
                '-d', '1', '-c', '2', '-t', '4', '-q', '--js=false', 
                '--output', 'gospider-output'],
                capture_output=True, text=True
        )),
            executor.submit(lambda: subprocess.run(
                ['gobuster', 'dir', '-u', 'http://juice-shop.local:3000', 
                '-w', 'common.txt', '-t', '5', '--exclude-length', '75002', 
                '-o', 'gobuster.txt'],
                capture_output=True, text=True
        ))
        ]
        print("Crawling...")
        wait(threads) #block until all threads are done
        print("Done")

def domain_flag(input_domain):
    with ThreadPoolExecutor(max_workers=3) as executor:  
        threads = [
            executor.submit(lambda: subprocess.run(
                ['nmap','-sV', '-sT', '-T3', '-oN', 'nmap.txt', input_domain],
                capture_output=True, text=True
        )),
            executor.submit(lambda: subprocess.run(                                              
                ['gospider', '-s', input_domain, 
                '-d', '1', '-c', '2', '-t', '4', '-q', 
                '--output', 'gospider-output'],
                capture_output=True, text=True
         )),
            executor.submit(lambda: subprocess.run(
                ['gobuster', 'dir', '-u', input_domain, 
                '-w', 'common.txt', '-t', '5',
                '-o', 'gobuster.txt'],
                capture_output=True, text=True
        ))
        ]
        print("Crawling...")
        wait(threads) #block until all threads are done
        print("Done")

def custom_flag():
    with open("commands.txt", "r") as file:
        commands = [line.strip() for line in file]


    with ThreadPoolExecutor(max_workers=3) as executor:  
        threads = [
            executor.submit(lambda: subprocess.run(
                ['nmap', commands[0], 'nmap.txt'],
                capture_output=True, text=True
            ))]
        



def add_argparse_fields():
    parser = argparse.ArgumentParser(description="Simple Bug Bounty Hunting Recon Tool")
    parser.add_argument("--tools", action="store_true", required=False, help="Display help menus for packaged recon tools")
    parser.add_argument("--test", action="store_true", required=False, help="Test recon tools against local OWASP Juice Shop (see README)")
    parser.add_argument("--domain", metavar=" {target domain}", required=False, help="Specify a target for all recon tools")
    parser.add_argument("--custom", action="store_true", required=False, help="Reads commands from 'commands.txt' and executes them in parallel")

    return parser.parse_args()
    
def main():
    #check_for_tools()
    args = add_argparse_fields()

    if args.test: test_flag()
    if args.tools: tools_flag()
    if args.domain: domain_flag(args.domain) #pass input to function
    if args.custom: custom_flag()

#main()
custom_flag()
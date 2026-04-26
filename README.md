# <h1 align="center">Bug-Bounty-Recon-Script</h1>

## Description
This script uses nmap, gospider and gobuster to perform non-intrusive recon on a target domain, intended for Bug Bounty Hunting.<br>

https://nmap.org/docs.html | https://github.com/jaeles-project/gospider | https://github.com/Oj/gobuster
    
### Script Flags
    FLAGS:
        --help: Display help menu for recon.py script
        --tools: Display help menus for packaged recon tools
        --test: Test recon tools against local OWASP Juice Shop (requires docker-compose up)
        --domain {target}: Specify a target for all recon tools
        --port {target port}: Specify a specific port for all recon tools 
        --custom: Reads commands from 'input/commands.txt' and executes them in parallel
        --shodan {target}: Query Shodan api against a target 

    RECON TOOL DEFAULT FLAGS:
        nmap -sV -sS -oN output/nmap.txt {target domain}
        gospider -s {target domain} -d 1 -c 2 -t 2 -q --output output/gospider-output
        gobuster gobuster dir -u {target domain} -w input/common.txt -t 1 -o output/gobuster.txt

## Installation

To test script against a legal target, you can optionally host OWASP Juice Shop:<br>
https://hub.docker.com/r/bkimminich/juice-shop#setup

Run docker pull bkimminich/juice-shop<br>
Run docker run --rm -p 3000:3000 bkimminich/juice-shop<br>
Browse to http://localhost:3000 (on macOS and Windows browse to http://192.168.99.100:3000 if you are using docker-machine instead of the native docker installation)<br>

If you would like to bundle OWASP juice-shop together with the script for testing, run the bellow commands:<br>

1. git clone https://github.com/rleviathan5/Bug-Bounty-Recon-Script.git
2. open a terminal in cloned repo
3. sudo docker-compose up --build -d<br>
4. open seperate terminal for ease
5. sudo docker exec -it script sh<br>

    at this point, if you 'ls' you'll see the repo files

6. python recon.py -h
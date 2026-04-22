# Bug-Bounty-Recon-Script
temporary readme layout, will prettify later<br>

This simple Bug Bounty Hunting script uses nmap, gospider and gobuster<br>
    https://nmap.org/docs.html | https://github.com/jaeles-project/gospider | https://github.com/Oj/gobuster<br>
    FLAGS:<br>
    --help: Display help menu for recon.py script<br>
    --tools: Display help menus for packaged recon tools<br>
    --test: Test recon tools against local OWASP Juice Shop (see README)<br>
    --domain {Valid Domain}: Specify a target for all recon tools<br>
    RECON TOOL DEFAULT FLAGS<br>
    nmap -sV -sS -oN nmap.txt {target domain}<br>
    gospider -s {target domain} -d 1 -c 2 -t 4 -q --output gospider-output<br>
    gobuster gobuster dir -u {target domain} -w common.txt -t 5 -o gobuster.txt<br>



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
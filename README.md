# Bug-Bounty-Recon-Script
temporary readme layout, will prettify later

To test script against a legal target, you can optionally host OWASP Juice Shop:<br>
https://hub.docker.com/r/bkimminich/juice-shop#setup

Run docker pull bkimminich/juice-shop<br>
Run docker run --rm -p 3000:3000 bkimminich/juice-shop<br>
Browse to http://localhost:3000 (on macOS and Windows browse to http://192.168.99.100:3000 if you are using docker-machine instead of the native docker installation)<br>

If you would like to bundle OWASP juice-shop together with the script for testing, run the bellow commands:<br>

1. open a terminal in cloned repo
2. sudo docker-compose up --build -d<br>
3. open seperate terminal for ease
4. sudo docker exec -it script sh<br>

    at this point, is you 'ls' you'll see the repo files

5. python recon.py -h
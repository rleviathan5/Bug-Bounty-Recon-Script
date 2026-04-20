# Bug-Bounty-Recon-Script
temporary readme layout, will prettify later

To test script against a legal target, you can optionally host OWASP Juice Shop:<br>
https://hub.docker.com/r/bkimminich/juice-shop#setup

Run docker pull bkimminich/juice-shop<br>
Run docker run --rm -p 3000:3000 bkimminich/juice-shop<br>
Browse to http://localhost:3000 (on macOS and Windows browse to http://192.168.99.100:3000 if you are using docker-machine instead of the native docker installation)<br>

For running the test flag, build your docker image with this command: <br>
sudo docker run -it --add-host host.docker.internal:host-gateway {your-image-name}

FROM python:3.8-slim

WORKDIR /home/abertay/Bug-Bounty-Recon-Script

COPY recon.py .

RUN apt-get update && apt-get install -y \
nmap \
gobuster \
&& rm -r -f /var/lib/apt/lists/*

CMD ["python", "-u", "recon.py"]

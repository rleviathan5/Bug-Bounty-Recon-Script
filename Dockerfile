#install go and gospider
FROM golang:1.22 AS builder
ENV GOBIN=/usr/local/bin
RUN GO111MODULE=on go install github.com/jaeles-project/gospider@latest

#install python, nmap and gobuster
FROM python:3.8-slim
RUN apt-get update && apt-get install -y \
nmap \
gobuster \
&& rm -r -f /var/lib/apt/lists/*
RUN pip install shodan

#move gospider to same dir as namp and gobuster
COPY --from=builder /usr/local/bin/gospider /usr/bin/gospider
WORKDIR /app
COPY recon.py .
COPY common.txt .



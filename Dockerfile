FROM python
WORKDIR /usr/src/app
COPY ./pscan6.py ./scan
RUN apt update && apt install -y arp-scan nmap
CMD [ "python3", "./scan"]

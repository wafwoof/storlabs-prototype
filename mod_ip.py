# Networking module for main.py
import os

def get_ip():
    # get ip address
    ip = os.popen('hostname -I').read()
    ip = ip.strip()
    # remove everything after the first space
    ip = ip.split(' ')[0]

    if ip == "":
        ip = os.popen('ipconfig getifaddr en0').read()
    if ip == "":
        ip = "xxx.xxx.xxx.xxx"

    return ip
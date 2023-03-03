# Networking module for main.py
import os

def get_ip():
    # get ip address
    ip = os.popen('hostname -I').read()
    ip = ip.strip()
    # remove everything after the first space
    ip = ip.split(' ')[0]
    return ip
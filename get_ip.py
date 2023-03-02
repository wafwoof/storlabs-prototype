# get local ip address
import os

def get_ip():
    # get ip address
    ip = os.popen('hostname -I').read()
    ip = ip.strip()
    return ip


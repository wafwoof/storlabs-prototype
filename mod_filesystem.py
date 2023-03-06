# Filesystem module for main.py
import shutil
import os

block0 = "█"
block1 = "▓"
block2 = "▒"
block3 = "░"


def get_total_disk_usage():
    # get disk usage
    total, used, free = shutil.disk_usage("/")
    # convert all to GB
    total = total // (2**30)
    used = used // (2**30)
    free = free // (2**30)
    return total, used, free
#▓ .wav / 0GB

def get_format_usage(directory, format):
    os.chdir("/")
    # list dir
    os.system("ls")

def block_status_bar(total, used):
    status_bar = ""

    # calculate usage percentage out of 100
    usage = int(used / total * 100)
    print("usage:", usage, "%")
    # for each 10% of usage, add a block
    while len(status_bar) < usage * 0.2:
        status_bar += block0

    while len(status_bar) < 20:
        status_bar += block3

    

    return status_bar
   
    

if __name__ == "__main__":
    import sys
    total, used, free = get_total_disk_usage()
    print(f"Total: {total}GB Used: {used}GB Free: {free}GB")
    print(f"Block Status: {block_status_bar(total, used)}")
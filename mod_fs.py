# Filesystem module for main.py
import shutil
from PIL import Image, ImageDraw, ImageFont
import os

block0 = "█"
block0 = "■"
block1 = "▓"
block2 = "▒"
block3 = "░"
block3 = "□"


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
    # total/used 
    status_bar = ""
    status_bar_length = 29
    # calculate percentage of disk used out of 100
    percent_used = (used / total) * 100
    # convert percent_used to equivalent fraction out of 29
    blocks_used = (percent_used / 100) * status_bar_length
    # round blocks_used to nearest integer
    blocks_used = round(blocks_used)
    # create status bar
    for i in range(0, blocks_used):
        status_bar += block0
    # if status_bar has no characters, add a single block3 anyways
    if len(status_bar) == 0:
        status_bar += block1
    for i in range(blocks_used, status_bar_length):
        status_bar += block3

    return status_bar

def get_directory(directory):
    # get output from ls command
    return os.popen(f"ls -l {directory}").read()
    

if __name__ == "__main__":
    total, used, free = get_total_disk_usage()
    print(f"Total: {total}GB Used: {used}GB Free: {free}GB")
    print(f"Block Status: {block_status_bar(total, used)}")
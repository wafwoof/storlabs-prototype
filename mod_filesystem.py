# Filesystem module for main.py
import shutil
import os, glob

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
def get_format_usage(format):
    os.chdir("/")
    total_size = 0
    # search for files with format
    for file in glob.glob(f"**/*.{format}", recursive=True):
        total_size += os.path.getsize(file)
    
    return f"{format} :", total_size // (2**30), "GB"

def block_status(percentage):
    if percentage >= 75:
        return block0
    elif percentage >= 50:
        return block1
    elif percentage >= 25:
        return block2
    else:
        return block3
    

if __name__ == "__main__":
    import sys
    total, used, free = get_total_disk_usage()
    print(f"Total: {total}GB Used: {used}GB Free: {free}GB")
    print(f"Block Status: {block_status(used)}")
    print(get_format_usage(sys.argv[1]))
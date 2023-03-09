# Project Storlabs Demonstration Software v0.02

import os
try:
    from waveshare_epd import epd2in9bc
except RuntimeError:
    print("Error importing epd2in9bc")
from PIL import Image, ImageDraw, ImageFont
import time
from mod_qrcode import *
from mod_ip import *
from mod_filesystem import *

pic_dir = 'pic'

def screen1():
    print("Drawing Screen 1", end=' ')
    # draw disk usage (right side of display)
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((135, 0), f"▓ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 32), f"▓ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 64), f"▓ .jpeg / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 96), f"▒ Used {used_disk}/{free_disk}GB", font=top_font, fill=0, align='left')

    # create and draw qr code (left side of display)
    # grab ip address
    ip = get_ip()
    create_qr(ip)
    qr = Image.open(os.path.join(pic_dir, 'qr.png'))
    bw_image_buffer.paste(qr, (16, 0))
    draw.text((16, 96), ip, font=info_font, fill=0, align='left')
    draw.text((16, 112), "Storlabs ©2023", font=info_font, fill=0, align='left')

    # clean up qr code file
    os.remove(os.path.join(pic_dir, 'qr.png'))

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done")

def screen2():
    print("Drawing Screen 2", end=' ')

    total_disk, used_disk, free_disk = get_total_disk_usage()
    block_status = block_status_bar(total_disk, used_disk)

    # draw disk usage (left side of display)
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((0, 0), f"▓ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 32), f"▓ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 64), f"▓ .jpeg / 0GB", font=top_font, fill=0, align='left')

    # draw disk usage (right side of display)
    draw.text((135, 0), f"▓ .flp / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 32), f"▓ .cr3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 64), f"▓ Total: {used_disk}/{free_disk}GB", font=top_font, fill=0, align='left')

    # draw block status bar (bottom of display)
    draw.text((0, 96), f"{block_status}", font=top_font, fill=0, align='left')

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done")

def screen3():
    # File Browser
    print("Drawing Screen 3", end=' ')
    dirname = '/'
    cursor0 = "▷"
    cursor1 = "▶"

    # ls just one file
    # ommit . and .. directories
    listing = os.popen('ls -a | grep -v "^.$" | grep -v "^..$"').read()
    # remove new line characters and split into array
    listing = listing.replace('\n', ', ')[:-2].split(', ')

    # draw browser options
    draw.text((3, 0), f"File Browser v0.01", font=header_font, fill=0, align='left')
    draw.text((3, 16), f"{cursor1}dir: {dirname}", font=info_font, fill=0, align='left')
    draw.text((3, 32), f"{cursor0}{len(listing)} Files", font=info_font, fill=0, align='left')

    # draw a vertical line between file list and file info
    draw.line((135, 0, 135, 128), fill=0, width=1)
    
    # loop through files and print to screen
    for i in range(len(listing)):
        draw.text((138, 0 + i * 12), f"{listing[i]}", font=info_font, fill=0, align='left')

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done")

def blank_screen():
    print("Blanking Screen", end=' ')
    draw.rectangle((0, 0, w, h), fill=255)
    #epd_disp.Clear() # takes too long
    print("done")

print("\n")
print("Project Storlabs Demonstration Software v0.02")


print("Initializing...", end=' ')
try:
    # init display
    epd_disp = epd2in9bc.EPD()
    epd_disp.init()

    # set w/h
    w = epd_disp.height
    h = epd_disp.width
    print("Width:", w, "Height:", h, end=' ')

    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 20)
    info_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 14)
    header_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 16)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer


    # set screen to blank
    blank_screen()

except Exception as error:
    print("Error initializing display,", end=' ')
    print(error, end='. ')

finally:
    print("done")
    
if __name__ == "__main__":
    while True:
        screen3()
        time.sleep(5)
        blank_screen()
        screen2()
        time.sleep(5)
        blank_screen()
        #screen1()
        #time.sleep(5)
        #blank_screen()



# make a partial update
#draw.rectangle((128, 0, 256, 32), fill=255)
#draw.text((128, 0), f"▓ .mp3 / 1GB", font=top_font, fill=0, align='left')
#epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)

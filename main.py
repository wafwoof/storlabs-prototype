# Project Storlabs Demonstration Software v0.03

import os
try:
    from waveshare_epd import epd2in9bc
except RuntimeError:
    print("Error importing epd2in9bc")
from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime, timezone, timedelta
from mod_qr import *
from mod_ip import *
from mod_fs import *

pic_dir = 'pic'
font = 'arial-unicode.ttf'

def screen1():
    # Default Screen
    print("Drawing Screen 1", end=' ')
    # draw disk usage (right side of display)
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((135, 0), f"■ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 32), f"■ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 64), f"■ .jpeg / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 96), f"■ Used {used_disk}/{free_disk}GB", font=top_font, fill=0, align='left')

    # create and draw qr code (left side of display)
    # grab ip address
    ip = get_ip()
    create_qr(ip)
    qr = Image.open(os.path.join(pic_dir, 'qr.png'))
    bw_image_buffer.paste(qr, (16, 2))
    draw.text((16, 96), ip, font=info_font, fill=0, align='left')
    draw.text((16, 112), "Storlabs ©2023", font=info_font, fill=0, align='left')

    # clean up qr code file
    os.remove(os.path.join(pic_dir, 'qr.png'))

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done.")

def screen2():
    # Disk Usage Overview
    print("Drawing Screen 2", end=' ')

    total_disk, used_disk, free_disk = get_total_disk_usage()
    block_status = block_status_bar(total_disk, used_disk)

    # draw disk usage (left side of display)
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((0, 0), f"■ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 32), f"■ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 64), f"■ .jpeg / 0GB", font=top_font, fill=0, align='left')

    # draw disk usage (right side of display)
    draw.text((135, 0), f"■ .flp / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 32), f"■ .cr3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 64), f"■ Total: {used_disk}/{free_disk}GB", font=top_font, fill=0, align='left')

    # draw block status bar (bottom of display)
    draw.text((0, 96), f"{block_status}", font=top_font, fill=0, align='left')

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done.")

def screen3():
    # File Browser
    print("Drawing Screen 3", end=' ')
    dirname = '/'
    cursor0 = "▷"
    cursor1 = "▶"
    cursor2 = "⇧"
    cursor3 = "⇩"

    # ls just one file
    # ommit . and .. directories
    listing = os.popen(f'ls {dirname} -a | grep -v "^.$" | grep -v "^..$"').read()
    # remove new line characters and split into array
    listing = listing.replace('\n', ', ')[:-2].split(', ')

    # draw browser options
    draw.text((3, 0), f"File Browser", font=top_font, fill=0, align='left')
    draw.text((3, 16), f"Viewing: {dirname}", font=top_font, fill=0, align='left')
    draw.text((3, 32), f"{len(listing) } Files", font=header_font, fill=0, align='left')
    draw.text((3, 48), f"{cursor1}Change Directory", font=info_font, fill=0, align='left')
    draw.text((3, 64), f"{cursor0}Refresh", font=info_font, fill=0, align='left')
    draw.text((3, 80), f"{cursor0}Quit to Menu", font=info_font, fill=0, align='left')


    # draw a vertical line between file list and file info
    draw.line((135, 0, 135, 128), fill=0, width=1)
    
    # loop through files and print to screen
    for i in range(len(listing)):
        draw.text((138, 0 + i * 12), f"{listing[i]}", font=header_font, fill=0, align='left')
    
    # draw upwards facing arrow at top of file list
    draw.text((w - 8, 0), f"{cursor2}", font=header_font, fill=0, align='left')
    # draw downwards facing arrow at bottom of file list
    draw.text((w - 8, 128 - 20), f"{cursor3}", font=header_font, fill=0, align='left')


    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done.")

def screen4(offset0: int, offset1: int):
    # Dual Clock
    print("Drawing Screen 4", end=' ')
    if offset0 == None:
        offset0 = -8
    if offset1 == None:
        offset1 = 8
    utc_time_0 = datetime.now(timezone.utc) + timedelta(hours=offset0)
    utc_time_1 = datetime.now(timezone.utc) + timedelta(hours=offset1)
    # add + to positive offsets
    if offset0 > 0:
        offset0 = f"+{offset0}"
    if offset1 > 0:
        offset1 = f"+{offset1}"

    # draw left clock
    draw.text((3, 0), f"Vancouver", font=header_font, fill=0, align='left')
    draw.text((3, 16), f"{utc_time_0.strftime('%H:%M:%S')}", font=header_font, fill=0, align='left')
    draw.text((3, 32), f"{utc_time_0.strftime('%d/%m/%Y')}", font=header_font, fill=0, align='left')
    draw.text((0, 48), f"UTC {offset0}", font=header_font, fill=0, align='left')

    # draw a vertical line between clocks
    draw.line((w / 2, 0, w / 2, 128), fill=0, width=1)

    # draw right clock
    draw.text((150, 0), f"Taipei", font=header_font, fill=0, align='left')
    draw.text((150, 16), f"{utc_time_1.strftime('%H:%M:%S')}", font=header_font, fill=0, align='left')
    draw.text((150, 32), f"{utc_time_1.strftime('%d/%m/%Y')}", font=header_font, fill=0, align='left')
    draw.text((150, 48), f"UTC {offset1}", font=header_font, fill=0, align='left')
    
    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    print("done.")

def blank_screen():
    print("Blanking Screen", end=' ')
    draw.rectangle((0, 0, w, h), fill=255)
    #epd_disp.Clear() # takes too long
    print("done.")

print("\n")
print("Project Storlabs Demonstration Software v0.03")


# Initialize Display
try:
    print("Initializing...", end=' ')
    # init display
    epd_disp = epd2in9bc.EPD()
    epd_disp.init()

    # set w/h
    w = epd_disp.height
    h = epd_disp.width
    print("Width:", w, "Height:", h, end=' ')

    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, font), 20)
    info_font = ImageFont.truetype(os.path.join(pic_dir, font), 14)
    header_font = ImageFont.truetype(os.path.join(pic_dir, font), 16)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer


    # set screen to blank
    blank_screen()

except Exception as error:
    print("Error initializing display,", end=' ')
    print(error, end='. ')

    print("Initializing in fallback mode", end=' ')

    # define epd_disp as dummy class that just displays the image buffer when epd_disp.display() is called
    class dummy_epd_disp:
        def display(self, image, red_image):
            image.show()
        def getbuffer(self, image):
            return image
    epd_disp = dummy_epd_disp()

    # set w/h
    w = 296
    h = 128
    print("Width:", w, "Height:", h, end=' ')

    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, font), 18)
    info_font = ImageFont.truetype(os.path.join(pic_dir, font), 14)
    header_font = ImageFont.truetype(os.path.join(pic_dir, font), 16)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer

    # set screen to blank
    blank_screen()

finally:
    print("done.")
    
if __name__ == "__main__":
    while True:
        screen4(-8, 8)
        blank_screen()
        #screen3()
        #blank_screen()
        #screen2()
        #blank_screen()
        #screen1()
        exit()
        #time.sleep(5)
        #blank_screen()
        #screen3()
        #time.sleep(5)
        #blank_screen()
        #screen2()
        #time.sleep(5)
        #blank_screen()
        #screen1()
        #time.sleep(5)
        #blank_screen()



# make a partial update
#draw.rectangle((128, 0, 256, 32), fill=255)
#draw.text((128, 0), f"▓ .mp3 / 1GB", font=top_font, fill=0, align='left')
#epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)

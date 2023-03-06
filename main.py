# Project Storlabs Demonstration Software v0.0.1

import os
from waveshare_epd import epd2in9bc
from PIL import Image, ImageDraw, ImageFont
import time
from mod_qrcode import *
from mod_ip import *
from mod_filesystem import *

pic_dir = 'pic'

def screen1():
    print("Drawing Screen 1")
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

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)
    # clean up qr code file
    os.remove(os.path.join(pic_dir, 'qr.png'))

def screen2():
    print("Drawing Screen 2")

    total_disk, used_disk, free_disk = get_total_disk_usage()
    block_status = block_status_bar(total_disk, used_disk)

    # draw disk usage (left side of display)
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((0, 0), f"▓ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 32), f"▓ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 64), f"▓ .jpeg / 0GB", font=top_font, fill=0, align='left')
    draw.text((0, 96), f"{block_status}", font=top_font, fill=0, align='left')
    draw.text((0, 96), f"Used {used_disk}/{free_disk}GB", font=top_font, fill=255, align='left')
    # draw disk usage (right side of display)
    draw.text((135, 0), f"▓ .r3d / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 32), f"▓ .cr3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((135, 64), f"▓ .flp / 0GB", font=top_font, fill=0, align='left')

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)

print("\n")
print("Project Storlabs Demonstration Software v0.0.1")


print("Initializing...", end=' ')
try:
    # init display
    epd_disp = epd2in9bc.EPD()
    epd_disp.init()

    # clear display
    epd_disp.Clear()

    # set w/h
    w = epd_disp.height
    h = epd_disp.width
    print("Width:", w, "Height:", h, end=' ')

    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 20)
    info_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 14)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer

except IOError as error:
    print(error)

finally:
    print("done")
    
if __name__ == "__main__":
    while True:
        screen1()
        time.sleep(5)
        draw.rectangle((0, 0, w, h), fill=255)
        screen2()
        time.sleep(5)
        draw.rectangle((0, 0, w, h), fill=255)



# make a partial update
#draw.rectangle((128, 0, 256, 32), fill=255)
#draw.text((128, 0), f"▓ .mp3 / 1GB", font=top_font, fill=0, align='left')
#epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)

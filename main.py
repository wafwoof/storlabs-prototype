# Project Storlabs Demonstration Software v0.0.1

import os
from waveshare_epd import epd2in9bc
from PIL import Image, ImageDraw, ImageFont
from mod_qrcode import *
from mod_ip import *
from mod_filesystem import *

pic_dir = 'pic'


print("\n")
print("Project Storlabs Demonstration Software v0.0.1")

print("Initializing...")
try:
    # init display
    epd_disp = epd2in9bc.EPD()
    epd_disp.init()

    # clear display
    epd_disp.Clear()

    # set w/h
    w = epd_disp.height
    h = epd_disp.width
    print("Width:", w, "Height:", h)

    # define fonts
    top_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 20)
    info_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 14)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer

    # draw disk usage
    total_disk, used_disk, free_disk = get_total_disk_usage()
    draw.text((128, 0), f"▓ .mp3 / 0GB", font=top_font, fill=0, align='left')
    draw.text((128, 32), f"▓ .wav / 0GB", font=top_font, fill=0, align='left')
    draw.text((128, 64), f"▓ .jpeg / 0GB", font=top_font, fill=0, align='left')
    draw.text((128, 96), f"▒ Used {used_disk}/{free_disk}GB", font=top_font, fill=0, align='left')

    # grab ip address
    ip = get_ip()
    print("IP:", ip)
    # create and draw qr code (left side of display)
    create_qr(ip)
    qr = Image.open(os.path.join(pic_dir, 'qr.png'))
    bw_image_buffer.paste(qr, (16, 0))
    draw.text((16, 96), ip, font=info_font, fill=0, align='left')
    draw.text((16, 112), "Storlabs ©2023", font=info_font, fill=0, align='left')


    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None) # todo: display only black image

    # make a partial update
    # draw white rectangle over the mp3 text
    draw.rectangle((128, 0, 128+128, 0+32), fill=255)
    draw.text((128, 0), f"▓ .mp3 / 1GB", font=top_font, fill=0, align='left')
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), None)

except IOError as error:
    print(error)

finally:
    print("program complete")
    # delete the qr code
    os.remove(os.path.join(pic_dir, 'qr.png'))



# Project Storlabs Demonstration Software v0.0.1

import os
from waveshare_epd import epd2in9bc
from PIL import Image, ImageDraw, ImageFont
import shutil
from create_qr import create_qr

pic_dir = 'pic'

def get_disk_usage():
    # get disk usage
    total, used, free = shutil.disk_usage("/")
    # convert all to GB
    total = total // (2**30)
    used = used // (2**30)
    free = free // (2**30)

    # format strings
    total = f"Total: {total} GB"
    used = f"Used: {used} GB"
    free = f"Free: {free} GB"

    return total, used, free

def get_ip():
    # get ip address
    ip = os.popen('hostname -I').read()
    ip = ip.strip()
    # remove everything after the first space
    ip = ip.split(' ')[0]
    return ip

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
    info_font = ImageFont.truetype(os.path.join(pic_dir, 'unifont.ttf'), 12)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer

    # draw disk usage
    total_disk, used_disk, free_disk = get_disk_usage()
    draw.text((130, 0), total_disk, font=top_font, fill=0, align='left')
    draw.text((130, 32), used_disk, font=top_font, fill=0, align='left')
    draw.text((130, 64), free_disk, font=top_font, fill=0, align='left')

    # grab ip address
    ip = get_ip()
    print("IP:", ip)
    # create and draw qr code (left side of display)
    create_qr(ip)
    qr = Image.open(os.path.join(pic_dir, 'qr.png'))
    bw_image_buffer.paste(qr, (16, 0))
    draw.text((16, 96), ip, font=info_font, fill=0, align='left')
    draw.text((16, 112), "Scan to connect!", font=info_font, fill=0, align='left')


    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), epd_disp.getbuffer(red_image_buffer)) # todo: display only black image
    #todo: experiment with partial updates and grayscale

except IOError as error:
    print(error)

finally:
    print("End of program")
    # delete the qr code
    os.remove(os.path.join(pic_dir, 'qr.png'))




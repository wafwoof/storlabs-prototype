# Project Storlabs Demonstration Software v0.0.1

import os
from waveshare_epd import epd2in9bc
from PIL import Image, ImageDraw, ImageFont
import shutil

pic_dir = 'pic'

def get_disk_usage():
    # get disk usage
    total, used, free = shutil.disk_usage("/")
    # convert all to GB
    total = total // (2**30)
    used = used // (2**30)
    free = free // (2**30)

    return total, used, free

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
    top_font = ImageFont.truetype(os.path.join(pic_dir, 'ComicMono.ttf'), 32)

    # define and draw background
    bw_image_buffer = Image.new(mode='1', size=(w, h), color=255) # b/w image buffer
    red_image_buffer = Image.new(mode='1', size=(w, h), color=255) # red image buffer
    draw = ImageDraw.Draw(bw_image_buffer) # method to draw on image buffer

    # position and draw text
    total_disk, used_disk, free_disk = get_disk_usage()
    draw.text((128, 0), total_disk, font=top_font, fill=0, align='center')
    draw.text((128, 0), used_disk, font=top_font, fill=0, align='center')
    draw.text((128, 0), free_disk, font=top_font, fill=0, align='center')

    # draw qr code png
    qr = Image.open(os.path.join(pic_dir, 'qr.png'))
    bw_image_buffer.paste(qr, (0, 0))

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(bw_image_buffer), epd_disp.getbuffer(red_image_buffer)) # todo: display only black image
    #todo: experiment with partial updates and grayscale

except IOError as error:
    print(error)




# Project Storlabs Demonstration Software v0.0.1

import os
from waveshare_epd import epd2in9bc
from PIL import Image, ImageDraw, ImageFont

pic_dir = 'pic'

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
    image = Image.new(mode='1', size=(w, h), color=255)
    draw = ImageDraw.Draw(image)

    # position and draw text
    draw.text((15, 0), 'Storlabs!', font=top_font, fill=0, align='left')

    # write buffer to display
    epd_disp.display(epd_disp.getbuffer(image), epd_disp.getbuffer(image))

except IOError as error:
    print(error)




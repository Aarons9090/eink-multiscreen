# !/usr/bin/python
# -*- coding:utf-8 -*-
import api.weatherdata as weather_api
import sys
import os
miscdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink-multiscreen/misc')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from lib.waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont

def main():

    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd4in2 Demo")

        epd = epd4in2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 35)

        Limage = Image.new('L', (epd.width, epd.height), "white")  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((10, 0), 'hello world', font=font24, fill="black")
        epd.display_4Gray(epd.getbuffer_4Gray(Limage))
        time.sleep(5)

        epd.Clear()
        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()


main()

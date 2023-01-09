# !/usr/bin/python
# -*- coding:utf-8 -*-
import api.weatherdata as weather_api
import sys
import os
miscdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink-multiscreen/misc')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import datetime
import logging
from lib.waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont

def main():

    logging.basicConfig(level=logging.DEBUG)

    try:
        date = datetime.datetime.now()
        datestr = date.strftime("%H:%M %A %d.%m.%Y")
        weatherdata = weather_api.get_weatherdata()
        temp = str(weatherdata["temp"])
       	epd = epd4in2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        print(os.path.join(miscdir, 'Font.ttc'))

        font57 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 57)
        font24 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 35)

        Limage = Image.new('L', (epd.width, epd.height), "white")  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)

        draw.rectangle((0,30,400,0), fill="black") 
        draw.text((10, 0), datestr, font=font24, fill="white")
        draw.text((121,39), f"{temp}°C", font=font57, fill="black")

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

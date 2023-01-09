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
       	epd = epd4in2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        print(os.path.join(miscdir, 'Font.ttc'))

        font53 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 53)
        font24 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 35)

        weather_test_icon = Image.open(os.path.join(miscdir, "weathertestbpm.bmp"))
        wind_icon = Image.open(os.path.join(miscdir, "windbmp.bmp"))
        drop_icon = Image.open(os.path.join(miscdir, "dropbmp.bmp"))

        while True:
            date = datetime.datetime.now()
            datestr = date.strftime("%H:%M %A %d.%m.%Y")
            weatherdata = weather_api.get_weatherdata()
            temp = str(weatherdata["temp"])
            precipitation = str(weatherdata["precipitation"])
            windspeed = str(weatherdata["windspeed"])

            Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Limage)

            draw.rectangle((0,30,400,0), fill="black") 
            draw.text((10, 0), datestr, font=font24, fill="white")
            Limage.paste(weather_test_icon, (7,41))
            draw.text((115,45), f"{temp}°C", font=font53, fill="black")
            Limage.paste(drop_icon, (282, 48))
            draw.text((312,47), f"{precipitation}%", font=font24, fill="black") 
            Limage.paste(wind_icon, (270, 82))
            draw.text((312,77), f"{windspeed}m/s", font=font24, fill="black")
            epd.display(epd.getbuffer(Limage))
            time.sleep(60)

        epd.Clear()
        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.Clear()
        epd4in2.epdconfig.module_exit()
        exit()


main()

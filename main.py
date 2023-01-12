# !/usr/bin/python
# -*- coding:utf-8 -*-
import api.weatherdata as weather_api
import api.nordnetdata as nordnet
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

        capital = "12345"
        max_change = "+123"
        today_change = "+12"

        while True:
            date = datetime.datetime.now()
            datestr = date.strftime("%H:%M %A %d.%m.%Y")
            temp = "0"
            precipitation = "0"
            windspeed = "0"

            try:
                weatherdata = weather_api.get_weatherdata()
                temp = str(weatherdata["temp"])
                precipitation = str(weatherdata["precipitation"])
                windspeed = str(weatherdata["windspeed"])
            except Expestion as e:
                print(e)
            #every 15 minutes, get nordnet data
            if int(date.strftime("%M")) % 5 == 0:
                print("getting nordnet data")
                nordnet_data = nordnet.get_account_data()
                capital = nordnet_data["capital"]
                max_change = nordnet_data["max_change"]
                today_change = nordnet_data["today_change"]
                print("nordnetdata:")
                print(nordnet_data)
            Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(Limage)
            # top bar
            draw.rectangle((0,30,400,0), fill="black") 
            draw.text((10, 0), datestr, font=font24, fill="white")
            # weather info
            Limage.paste(weather_test_icon, (7,41))
            draw.text((115,45), f"{temp}°C", font=font53, fill="black")
            Limage.paste(drop_icon, (282, 48))
            draw.text((312,47), f"{precipitation}%", font=font24, fill="black") 
            Limage.paste(wind_icon, (270, 82))
            draw.text((312,77), f"{windspeed}m/s", font=font24, fill="black")

            # nordnet info
            draw.rectangle((0,300,400,131), fill="black")
            draw.text((286, 138), "Nordnet:", font=font24, fill="white")
            draw.text((267, 171), "Total", font=font18, fill="white")
            draw.text((271, 196), "Max", font=font18, fill="white")
            draw.text((283, 221), "1D", font=font18, fill="white")

            draw.text((321, 171), f"{capital}€", font=font18, fill="white")
            draw.text((332, 196), f"{max_change}€", font=font18, fill="white")
            draw.text((342, 221), f"{today_change}€", font=font18, fill="white")

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

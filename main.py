# !/usr/bin/python
# -*- coding:utf-8 -*-
import api.weatherdata as weather_api
import api.nordnetdata as nordnet
import api.weathericons as weathericons
import sys
import os
import datetime
import logging
from lib.waveshare_epd import epd4in2
import time
from PIL import Image, ImageDraw, ImageFont

miscdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'eink-multiscreen/misc')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


def is_stockmarket_open(hour):
    if 9 <= hour <= 21:
        return True
    return False


def main():
    logging.basicConfig(level=logging.DEBUG)

    try:
        epd = epd4in2.EPD()
        epd.init()
        epd.Clear()

        # fonts
        iconfont = ImageFont.truetype(os.path.join(miscdir, 'meteocons.ttf'), 77)
        bold24 = ImageFont.truetype(os.path.join(miscdir, 'segoeuibold.ttf'), 24)
        font21 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 21)
        font24 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 24)
        font53 = ImageFont.truetype(os.path.join(miscdir, 'Font.ttc'), 53)

        wind_icon = Image.open(os.path.join(miscdir, "windbmp.bmp"))
        drop_icon = Image.open(os.path.join(miscdir, "dropbmp.bmp"))

        # default values for weather data
        temp = "0"
        precipitation = "0"
        windspeed = "0"
        weathercode = 0

        # default values for nordnet data
        capital = "12 345"
        max_change = "+123"
        today_change = "+12"

        # event loop
        while True:
            date = datetime.datetime.now()
            timestr = date.strftime("%H:%M")
            day_of_week = date.strftime("%A")
            datestr = date.strftime("%d.%m.%Y")

            # fetch weather data
            try:
                weatherdata = weather_api.get_weatherdata()
                temp = str(weatherdata["temp"])
                precipitation = str(weatherdata["precipitation"])
                windspeed = str(weatherdata["windspeed"])
                weathercode = weatherdata["weathercode"]
            except Exception as e:
                print("Failed getting weather data: ", e)

            # get nordnet data only when the stock exchange is open and only once an hour
            if int(date.strftime("%M")) == 0 and is_stockmarket_open(int(date.strftime("%H"))):
                print("getting nordnet data")
                nordnet_data = nordnet.get_account_data()
                capital = nordnet_data["capital"]
                max_change = nordnet_data["max_change"]
                today_change = nordnet_data["today_change"]
                print("nordnetdata:")
                print(nordnet_data)

            image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
            draw = ImageDraw.Draw(image)

            # top bar
            draw.rectangle((0, 30, 400, 0), fill="black")
            draw.text((10, 0), timestr, font=font24, fill="white")
            draw.text((80, -3), day_of_week, font=bold24, fill="white")
            draw.text((195, 0), datestr, font=font24, fill="white")

            # weather info
            draw.text((10, 41), weathericons.get_weathericon(weathercode), font=iconfont)
            draw.text((115,45), f"{temp}°C", font=font53, fill="black")
            image.paste(drop_icon, (272, 48))
            draw.text((312,47), f"{precipitation}%", font=font24, fill="black") 
            image.paste(wind_icon, (260, 82))
            draw.text((312,77), f"{windspeed}m/s", font=font24, fill="black")

            # nordnet info
            draw.rectangle((0,300,400,131), fill="black")
            draw.text((259, 135), "Nordnet:", font=bold24, fill="white")
            draw.text((259, 166), "Total", font=font21, fill="white")
            draw.text((263, 192), "Max", font=font21, fill="white")
            draw.text((276, 217), "1D", font=font21, fill="white")

            draw.text((321, 167), f"{capital}€", font=font21, fill="white")
            draw.text((336, 192), f"{max_change}€", font=font21, fill="white")
            draw.text((347, 217), f"{today_change}€", font=font21, fill="white")

            # display image
            epd.display(epd.getbuffer(image))
            time.sleep(60)

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.Clear()
        epd4in2.epdconfig.module_exit()
        exit()


main()

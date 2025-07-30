import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

from monitor_module import MonitorModule
from resource_module import ResourceModule

HEIGHT = 64
WIDTH = 128
#dht11_pin = board.D14
#oled_reset_pin = board.D4
oled_reset = digitalio.DigitalInOut(board.D4)
# Load default font.
font = ImageFont.load_default()
oled = None


def initialize_display():
    global oled
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

    oled.fill(0)
    oled.show()

def test_display():
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,WIDTH,HEIGHT), outline=0, fill=0)
    draw.text((10, 10), str('Hello World'),  font=font, fill=255)
    oled.image(image)
    oled.show()


if __name__ == "__main__":
    initialize_display()
    #monitormodule = MonitorModule()
    resourcemodule = ResourceModule()
    while True:
        #monitormodule.display_monitor(oled)
        resourcemodule.resource_monitor(oled)
        time.sleep(resourcemodule.LOOPTIME)
        print("Display updated")

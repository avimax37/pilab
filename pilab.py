import time
import board
import digitalio
import adafruit_ssd1306

from resource_module import ResourceModule
from dht11_module import DHT11Module
from network_module import NetworkModule

HEIGHT = 64
WIDTH = 128
oled_reset = digitalio.DigitalInOut(board.D4)
oled = None

def initialize_display():
    global oled
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
    oled.fill(0)
    oled.show()

if __name__ == "__main__":
    initialize_display()
    resourcemodule = ResourceModule()
    dhtmodule = DHT11Module()
    networkmodule = NetworkModule()

    while True:
        # Show Resource Module for 5 seconds
        start = time.time()
        while time.time() - start < 5:
            resourcemodule.resource_monitor(oled)

        # Show Network Module for 5 seconds
        start = time.time()
        while time.time() - start < 5:
            networkmodule.network_display(oled)

        # Show DHT11 Module for 5 seconds
        start = time.time()
        while time.time() - start < 5:
            dhtmodule.dht_display(oled)
import time
import board
import adafruit_dht
import os

from PIL import Image, ImageDraw, ImageFont


class DHT11Module:
    def __init__(self):
        self.dht_device = adafruit_dht.DHT11(board.D17)
        self.LOOPTIME = 1.0  # Delay between readings

    def dht_display(self, oled):
        width = oled.width
        height = oled.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        padding = -2
        top = padding
        bottom = height - padding
        x = 0

        # Font loading
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelOperator.ttf")
        icon_font_path = os.path.join(os.path.dirname(__file__), "fonts", "lineawesome-webfont.ttf")

        # font size 24
        try:
            font = ImageFont.truetype(font_path, 24)
        except (IOError, OSError):
            print("Warning: PixelOperator.ttf not found. Using default font.")
            font = ImageFont.load_default()

        # icon size 24
        try:
            icon_font = ImageFont.truetype(icon_font_path, 24)
        except (IOError, OSError):
            print("Warning: lineawesome-webfont.ttf not found. Using default font.")
            icon_font = ImageFont.load_default()

        try:
            # Attempt sensor read
            temperature_c = self.dht_device.temperature
            humidity = self.dht_device.humidity

            if temperature_c is None or humidity is None:
                raise RuntimeError("Sensor returned None")

            temp_text = f"{temperature_c:.1f}'C"
            humidity_text = f"{humidity:.1f}% RH"

        except RuntimeError as e:
            temp_text = "Temp: --"
            humidity_text = "Hum: --"
            print(f"[DHT11 Error] {e}")

        # Draw icons
        # Temperature icon
        draw.text((x, top + 10), chr(0xf2c7), font=icon_font, fill=255)  
        # Humidity icon
        draw.text((x, top + 40), chr(0xf043), font=icon_font, fill=255)  

        # Draw text values
        draw.text((x + 25, top + 8), temp_text, font=font, fill=255)
        draw.text((x + 25, top + 38), humidity_text, font=font, fill=255)

        # Display update
        oled.image(image)
        oled.show()
        time.sleep(self.LOOPTIME)
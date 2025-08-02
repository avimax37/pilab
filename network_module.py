import time
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

class NetworkModule:
    def __init__(self):
        self.LOOPTIME = 1.0  # Delay between updates

    def get_output(self, cmd, fallback="N/A"):
        try:
            return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        except Exception as e:
            print(f"[NetworkModule Error] {e}")
            return fallback

    def get_interface_status(self, interface="wlan0"):
        output = self.get_output(f"cat /sys/class/net/{interface}/operstate", fallback="unknown")
        return output.upper()

    def get_ip(self):
        return self.get_output("hostname -I | cut -d' ' -f1")

    def get_ssid(self):
        return self.get_output("iwgetid -r")

    def network_display(self, oled):
        width = oled.width
        height = oled.height
        image = Image.new("1", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        padding = -2
        top = padding
        bottom = height - padding
        x = 0

        # Font loading
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelOperator.ttf")
        icon_font_path = os.path.join(os.path.dirname(__file__), "fonts", "lineawesome-webfont.ttf")

        # font size 18
        try:
            font = ImageFont.truetype(font_path, 18)
        except (IOError, OSError):
            print("Warning: PixelOperator.ttf not found. Using default font.")
            font = ImageFont.load_default()

        # icon size 18
        try:
            icon_font = ImageFont.truetype(icon_font_path, 18)
        except (IOError, OSError):
            print("Warning: lineawesome-webfont.ttf not found. Using default font.")
            icon_font = ImageFont.load_default()

        ssid = self.get_ssid()
        ip = self.get_ip()
        status = self.get_interface_status()

        

        # Draw icons
        # SSID icon
        draw.text((x, top + 10), chr(0xf796), font=icon_font, fill=255)  
        # IP icon
        draw.text((x, top + 20), chr(0xf1eb), font=icon_font, fill=255)
        # Status icon
        draw.text((x, top + 30), chr(0xf012), font=icon_font, fill=255)

        # Draw text values
        draw.text((x + 10, top + 10), ssid, font=font, fill=255)
        draw.text((x + 10, top + 20), ip, font=font, fill=255)
        draw.text((x + 10, top + 30), status, font=font, fill=255)

        oled.image(image)
        oled.show()
        time.sleep(self.LOOPTIME)
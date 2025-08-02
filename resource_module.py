import time
import board
import busio
import digitalio
import os

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess


class ResourceModule:
    def __init__(self):
        # Display Refresh
        self.LOOPTIME = 1.0

    def get_output(self, cmd, fallback="N/A"):
        try:
            return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Command failed: {cmd}\nError: {e}")
            return fallback
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return fallback

    def resource_monitor(self, oled):
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

        # icon size 24 for temperature
        try:
            icon_font_temp = ImageFont.truetype(icon_font_path, 24)
        except (IOError, OSError):
            print("Warning: lineawesome-webfont.ttf (temp) not found. Using default font.")
            icon_font_temp = ImageFont.load_default()

        # System stats
        IP = self.get_output("hostname -I | cut -d' ' -f1 | head --bytes -1")
        
        # CPU usage using mpstat (as requested, unchanged)
        CPU_Perc = self.get_output("mpstat 1 1 | awk '/Average/ {print 100 - $NF}'")
        try:
            cpu_str = "{:.1f}%".format(float(CPU_Perc))
        except ValueError:
            cpu_str = "--%"

        MemUsage = self.get_output("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'")
        Disk = self.get_output("df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'")
        Temperature = self.get_output("vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1")

        # Draw icons
        # Temperature icon
        draw.text((x + 93, top + 12), chr(0xf2c7), font=icon_font_temp, fill=255)  
        # Memory icon
        draw.text((x, top + 10), chr(0xf538), font=icon_font, fill=255)    
        # Disk icon  
        draw.text((x, top + 29), chr(63426), font=icon_font, fill=255)     
        # CPU icon       
        draw.text((x, top + 49), chr(62171), font=icon_font, fill=255)             

        # Draw text values
        draw.text((x + 82, top + 38), Temperature, font=font, fill=255)
        draw.text((x + 19, top + 8), MemUsage, font=font, fill=255)
        draw.text((x + 19, top + 28), Disk, font=font, fill=255)
        draw.text((x + 19, top + 48), cpu_str, font=font, fill=255)

        # Optional: draw IP address (uncomment if needed)
        # draw.text((x + 19, top + 58), IP, font=font, fill=255)

        draw.line((75, 0, 75, height - 1), fill=255)

        # Display image
        oled.image(image)
        oled.show()
        time.sleep(self.LOOPTIME)

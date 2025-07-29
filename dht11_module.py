import time
import board
import busio
import adafruit_ssd1306
import adafruit_dht

class DHT11Module:
    def __init__(self, pin):
        # Initialize the DHT11 sensor on the specified data pin
        self.dht_device = adafruit_dht.DHT11(pin)

    def read_sensor(self):
        try:
            # Get temperature and humidity readings
            temperature_c = self.dht_device.temperature
            humidity = self.dht_device.humidity

            # Convert temperature to Fahrenheit
            temperature_f = temperature_c * (9 / 5) + 32

            return temperature_c, temperature_f, humidity

        except RuntimeError as error:
            # Handle sensor reading errors
            print(f"Error reading sensor: {error.args[0]}")
            return None, None, None

    def display_readings(self, oled):
        # Read sensor data
        temperature_c, temperature_f, humidity = self.read_sensor()

        if temperature_c is not None and humidity is not None:
            # Clear the display
            oled.fill(0)
            oled.show()

            # Create a blank image for drawing
            image = Image.new("1", (oled.width, oled.height))
            draw = ImageDraw.Draw(image)

            # Load a font (or use default)
            font = ImageFont.load_default()

            # Draw the readings on the image
            draw.text((0, 0), f"Temp={temperature_c:.1f}ºC", font=font, fill=255)
            draw.text((0, 10), f"Temp={temperature_f:.1f}ºF", font=font, fill=255)
            draw.text((0, 20), f"Humidity={humidity:.1f}%", font=font, fill=255)

            # Display the image on the OLED
            oled.image(image)
            oled.show()
        else:
            print("Failed to read sensor data.")

    def close(self):
        self.dht_device.exit()  # Clean up the DHT device
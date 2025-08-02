import time
import board
import busio
import adafruit_bmp280

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create BMP280 sensor object
# Default I2C address is 0x76, but some modules might use 0x77
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Optional: Set sea-level pressure for accurate altitude calculation
# Replace 1013.25 with your local sea-level pressure in hPa/millibars
bmp280.sea_level_pressure = 1013.25

try:
    while True:
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        altitude = bmp280.altitude

        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Altitude: {altitude:.2f} m")
        print("-" * 30)
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting sensor readings.")
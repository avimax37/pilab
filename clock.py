import gpiod
import time
from gpiod import LineSettings, LineDirection, LineValue

class TM1637:
    def __init__(self, clk_pin, dio_pin, chip='/dev/gpiochip0'):
        self.clk_pin = clk_pin
        self.dio_pin = dio_pin
        self.chip = gpiod.Chip(chip)

        self._config_output = LineSettings()
        self._config_output.direction = LineDirection.OUTPUT
        self._config_output.output_value = LineValue.ACTIVE

        self._config_input = LineSettings()
        self._config_input.direction = LineDirection.INPUT

        self._request_lines()

    def _request_lines(self):
        self.clk_line = self.chip.request_lines(
            consumer='tm1637-clk',
            config={self.clk_pin: self._config_output}
        )
        self.dio_line = self.chip.request_lines(
            consumer='tm1637-dio',
            config={self.dio_pin: self._config_output}
        )

    def _set_clk(self, val): self.clk_line.set_value({self.clk_pin: val})
    def _set_dio(self, val): self.dio_line.set_value({self.dio_pin: val})

    def _release_dio(self):
        self.dio_line.release()
        self.dio_line = self.chip.request_lines(
            consumer='tm1637-dio-in',
            config={self.dio_pin: self._config_input}
        )

    def _acquire_dio(self):
        self.dio_line.release()
        self.dio_line = self.chip.request_lines(
            consumer='tm1637-dio-out',
            config={self.dio_pin: self._config_output}
        )

    def _start(self):
        self._set_dio(1)
        self._set_clk(1)
        time.sleep(0.00001)
        self._set_dio(0)
        time.sleep(0.00001)
        self._set_clk(0)

    def _stop(self):
        self._set_clk(0)
        self._set_dio(0)
        time.sleep(0.00001)
        self._set_clk(1)
        time.sleep(0.00001)
        self._set_dio(1)

    def _write_byte(self, b):
        for i in range(8):
            self._set_clk(0)
            self._set_dio((b >> i) & 1)
            time.sleep(0.00001)
            self._set_clk(1)
            time.sleep(0.00001)

        # Read ACK
        self._set_clk(0)
        self._release_dio()
        self._set_clk(1)
        time.sleep(0.00001)
        self._set_clk(0)
        self._acquire_dio()

    def write(self, data):
        self._start()
        self._write_byte(0x40)  # auto-increment mode
        self._stop()

        self._start()
        self._write_byte(0xC0)  # address 0x00
        for b in data:
            self._write_byte(b)
        self._stop()

        self._start()
        self._write_byte(0x88 | 0x07)  # display on, brightness 7
        self._stop()


# Pin config for Raspberry Pi 5
CLK = 4     # BCM 4 (Pin 7)
DIO = 27    # BCM 27 (Pin 13)

tm = TM1637(clk_pin=CLK, dio_pin=DIO)

# Display "88:88"
tm.write([0x7F, 0xFF, 0x7F, 0x7F])

# SPDX-FileCopyrightText: 2020 Foamyguy, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Foamyguy for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_monsterm4sk`
================================================================================

Helper library for the Monster M4sk device. Allows usage of screens and other built-in hardware.


* Author(s): Foamyguy

Implementation Notes
--------------------

**Hardware:**

* `MONSTER M4SK <https://www.adafruit.com/product/4343>`


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases


# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
import time
import board
import busio
import pulseio
import digitalio
from adafruit_seesaw.seesaw import Seesaw
import displayio
import touchio
from adafruit_st7789 import ST7789
import adafruit_lis3dh

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MonsterM4sk.git"

SS_LIGHTSENSOR_PIN = 2
SS_VCCSENSOR_PIN = 3
SS_BACKLIGHT_PIN = 5
SS_TFTRESET_PIN = 8
SS_SWITCH1_PIN = 9
SS_SWITCH2_PIN = 10
SS_SWITCH3_PIN = 11


class MonsterM4sk:
    """Class representing a `MONSTER M4SK`
           <https://www.adafruit.com/product/4343>`_.

            The terms "left" and "right" are always used from the
            perspective of looking out of the mask.
            The right screen is the one USB port directly above it.
           """

    def __init__(self, i2c=None):
        displayio.release_displays()

        if i2c is None:
            i2c = board.I2C()

        # set up on-board seesaw
        self._ss = Seesaw(i2c)
        # left screen
        self._ss.pin_mode(SS_TFTRESET_PIN, self._ss.OUTPUT)
        self._ss.pin_mode(SS_SWITCH1_PIN, self._ss.INPUT_PULLUP)
        self._ss.pin_mode(SS_SWITCH2_PIN, self._ss.INPUT_PULLUP)
        self._ss.pin_mode(SS_SWITCH3_PIN, self._ss.INPUT_PULLUP)

        self._ss.pin_mode(SS_LIGHTSENSOR_PIN, self._ss.INPUT)

        # Manual reset for left screen
        self._ss.digital_write(SS_TFTRESET_PIN, False)
        time.sleep(0.01)
        self._ss.digital_write(SS_TFTRESET_PIN, True)
        time.sleep(0.01)

        # Left backlight pin, on the seesaw
        self._ss.pin_mode(SS_BACKLIGHT_PIN, self._ss.OUTPUT)
        # backlight on full brightness
        self._ss.analog_write(SS_BACKLIGHT_PIN, 255)

        # Left screen spi bus
        left_spi = busio.SPI(board.LEFT_TFT_SCK, MOSI=board.LEFT_TFT_MOSI)
        left_tft_cs = board.LEFT_TFT_CS
        left_tft_dc = board.LEFT_TFT_DC

        left_display_bus = displayio.FourWire(
            left_spi, command=left_tft_dc, chip_select=left_tft_cs
        )

        self.left_display = ST7789(left_display_bus, width=240, height=240, rowstart=80)

        self.right_backlight = pulseio.PWMOut(
            board.RIGHT_TFT_LITE, frequency=5000, duty_cycle=0
        )
        self.right_backlight.duty_cycle = 65535

        # right display
        right_spi = busio.SPI(board.RIGHT_TFT_SCK, MOSI=board.RIGHT_TFT_MOSI)
        right_tft_cs = board.RIGHT_TFT_CS
        right_tft_dc = board.RIGHT_TFT_DC

        right_display_bus = displayio.FourWire(
            right_spi,
            command=right_tft_dc,
            chip_select=right_tft_cs,
            reset=board.RIGHT_TFT_RST,
        )

        self.right_display = ST7789(
            right_display_bus, width=240, height=240, rowstart=80
        )

        if i2c is not None:
            int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
            try:
                self._accelerometer = adafruit_lis3dh.LIS3DH_I2C(
                    i2c, address=0x19, int1=int1
                )
            except ValueError:
                self._accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

        self.nose = touchio.TouchIn(board.NOSE)
        self.nose.threshold = 180

    @property
    def acceleration(self):
        """Accelerometer data, +/- 2G sensitivity."""
        return (
            self._accelerometer.acceleration
            if self._accelerometer is not None
            else None
        )

    @property
    def light(self):
        """Light sensor data."""
        return self._ss.analog_read(SS_LIGHTSENSOR_PIN)

    @property
    def boop(self):
        """Nose touch sense."""
        return self.nose.value

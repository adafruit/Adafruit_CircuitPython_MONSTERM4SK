Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-monsterm4sk/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/monsterm4sk/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_MonsterM4sk/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_MonsterM4sk/actions
    :alt: Build Status

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

Helper library for the Monster M4sk device. Allows usage of screens and other built-in hardware.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_
* `Seesaw <https://github.com/adafruit/Adafruit_CircuitPython_seesaw>`_
* `LIS3DH <https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH>`_
* `ST7789 <https://github.com/adafruit/Adafruit_CircuitPython_ST7789>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library will not be available on PyPI. Install documentation is included
   as a standard element.


Usage Example
=============

.. code-block:: python

    import board
    import displayio
    from adafruit_display_shapes.circle import Circle
    import adafruit_monsterm4sk

    SCREEN_SIZE = 240

    i2c_bus = board.I2C()

    mask = adafruit_monsterm4sk.MonsterM4sk(i2c=i2c_bus)

    left_group = displayio.Group()
    mask.left_display.root_group = left_group

    right_group = displayio.Group()
    mask.right_display.root_group = right_group

    right_circle = Circle(SCREEN_SIZE // 2, SCREEN_SIZE // 2, 40, fill=0x0000FF)
    right_group.append(right_circle)

    left_circle = Circle(SCREEN_SIZE // 2, SCREEN_SIZE // 2, 40, fill=0x00AA66)
    left_group.append(left_circle)
    while True:
        pass

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/monsterm4sk/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_MonsterM4sk/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

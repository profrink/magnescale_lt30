# Read data from measurement device Magnescale LT30
#
# @author = "Andre Wiegleb"

# __copyright__ = "Copyright 2022, The Calibration Project"
# __credits__ = [""]
"""
__filename__ = 'magnescale_lt30.py'
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Andre Wiegleb"
__email__ = "andre.wiegleb@mts.com"
__status__ = "Development"
"""

import serial
from time import sleep


class LT30:
    """Read values from LT30"""
    def __init__(self, port=None):
        self.port = port
        self.ser_obj = serial.Serial(self.port,
                                     baudrate='9600',
                                     bytesize=8,
                                     stopbits=1,
                                     parity='N',
                                     timeout=0)
        self.cycles = 1

    def tare(self):
        """
        RESET LT30 to Zero
        """
        self.ser_obj.write(b"*RES\r")

    def read(self):
        """
        Read value(s) from LT30

        :return: str value
        """
        value = ''
        for i in range(self.cycles):
            self.ser_obj.write(b"*r\r\n")
            sleep(0.01)
            value = (self.ser_obj.readline()[1:-2].decode())
        return value

    def close(self):
        """
        deletes the ser_obj and closes serial port.

        Port should always be closed when ready
        """
        del self.ser_obj

    def flush(self):
        self.ser_obj.flushInput()
        self.ser_obj.flushOutput()

    def test(self):
        sleep(0.5)
        self.ser_obj.write(b"*r\r\n")
        sleep(0.01)
        value = (self.ser_obj.readline().decode())
        # check if we have response from LT30
        # self.close()
        if (value[:1] + value[-2:]) == 'A\r\n':
            return self.port

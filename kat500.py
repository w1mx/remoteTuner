#!/usr/bin/env python3

"""
Library for interfacing with the Elecraft KAT500 automatic antenna tuner over serial. Written by Oliver Trevor (KM6WOX) for MIT Radio Society (W1MX) station use.
"""

import time
import serial

# Possible baud rates used by the KAT500 antenna tuner. Defaults to BR3 if baud rate has not been changed.
BR0 = 4800
BR1 = 9600
BR2 = 19200
BR3 = 38400

class KAT500:
    """
    Class to interface the Elecraft KAT500 antenna tuner over serial. See https://ftp.elecraft.com/KAT500/Manuals%20Downloads/KAT500%20Automatic%20Antenna%20Tuner%20Serial%20Command%20Reference.pdf for documentation of serial protocol.
    """
    def __init__(self, serial_port_device = "/dev/ttyTuner", baud_rate = None):
        """
        Initialize the antenna tuner. serial_port_device is the path (or COM port on Windows) to the tuner. baud_rate is the desired baud rate (can be BR0, BR1, BR2, BR3, or None). BR0 is 4800 baud, BR1 is 9600 baud, BR2 is 19200 baud, BR3 is 38400 baud, and None will cause the library to attempt to auto-discover the baudrate by sending null commands until the tuner responds. Using None is recommended.
        """
        self.serial_port = None
        # Auto-discover baud rate if not provided.
        if baud_rate is None:
            correct_baud_rate = None
            # Try baud rates until we get a response.
            for baud_rate in [BR0, BR1, BR2, BR3]:
                s = serial.Serial(serial_port_device, baud_rate)
                for _ in range(5):
                    s.write(b';')
                    time.sleep(0.1)
                if s.in_waiting:
                    correct_baud_rate = baud_rate
                    break
                s.close()
            # If there was no response on any baud rate, throw an error.
            if correct_baud_rate is None:
                raise IOError("Could not get KAT500 to respond with any of the possible baud rates. Verify that serial connection and port are correct.")
        # Use the provided baud rate.
        else:
            correct_baud_rate = baud_rate
        # Initialize serial port.
        self.serial_port = serial.Serial(serial_port_device, correct_baud_rate)
        # Read some basic information about the tuner and print it out.
        print("KAT500 Firmware Revision: {}".format(self.get_firmware_revision()))

    def _read_response(self):
        """
        Helper method to read a response from the tuner on serial. Reads until a ';' character is received. Blocking.
        """
        response_buffer = self.serial_port.read(1)
        while response_buffer[-1] != b';'[0]:
            bytes_read = self.serial_port.read(self.serial_port.in_waiting)
            response_buffer += bytes_read
        return response_buffer.decode()[0:-1]

    def get_firmware_revision(self):
        """
        Use the 'RV;' command to get the firmware revision.
        """
        self.serial_port.write(b"RV;")
        return self._read_response().replace("RV", '')

    def get_vswr(self):
        """
        Use the 'VSWR;' command to get the VSWR (Voltage Standing Wave Ratio, a measure of how well-tuned the antenna is). Returns a float.
        """
        self.serial_port.write(b"VSWR;")
        return float(self._read_response().replace("VSWR ", ''))

    def __del__(self):
        """
        Destroy this instance of the class, closing the serial port if necessary.
        """
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None

if __name__ == "__main__":
    kat500 = KAT500(baud_rate = 38400)

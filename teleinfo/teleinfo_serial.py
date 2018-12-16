#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import logging
import sys
import time
import copy

class Teleinfo_serial:

        ser = serial.Serial()

        def __init__ (self, port='/dev/ttyUSB0'):
                try:
                  self.port=port
                  self.ser = serial.Serial()
                except OSError as e:
                  logging.critical('Could not open serial port : %s',e)
                  sys.exit(1)

                try:
                  self.ser.baudrate = 1200
                  self.ser.port = port
                  self.ser.parity = serial.PARITY_EVEN
                  self.ser.bytesize = serial.SEVENBITS
                  self.ser.open()
                except serial.SerialException as e:
                  logging.critical('Could not open serial port {}: {}\n'.format(self.ser.name, e))
                  sys.exit(1)

                time.sleep(1)


        def checksum (self, etiquette, valeur):
                sum = 32
                for c in etiquette: sum = sum + ord(c)
                for c in valeur:        sum = sum + ord(c)
                sum = (sum & 63) + 32
                #print 'checksum of %s %s is %c' %(etiquette,valeur,sum)
                return chr(sum)

        def read(self, pattern):

          data = copy.copy(pattern)
          while 'O' in data.values():
            message = self.ser.readline()

            frames = [ filter(None,frame.split(" ")) for frame in message.strip("\r\n\x03").split("\r\n")]
            for frame in frames:
              if( ((len(frame) == 3) and (self.checksum(frame[0],frame[1]) == frame[2])) or (len(frame) == 2)):
                data[frame[0]] = frame[1]
              else:
                logging.debug('invalid checksum frame %s' %(frame))
                continue
          return data

        def close (self):
          self.ser.close()



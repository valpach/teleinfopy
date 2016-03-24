#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import logging
import sys
import time

TEMPO_TI={
  'ADCO':'O',
  'OPTARIF':'O',
  'ISOUSC':'O',
  'BASE':'N',
  'HCHC':'N',
  'HCHP':'N',
  'EJPHN':'N',
  'EJPHPM':'N',
  'BBRHCJB':'O',
  'BBRHPJB':'O',
  'BBRHCJW':'O',
  'BBRHPJW':'O',
  'BBRHCJR':'O',
  'BBRHPJR':'O',
  'PEJP':'N',
  'PTEC':'O',
  'DEMAIN':'O',
  'IINST':'O',
  'IINST2':'',
  'IINST3':'',
  'IMAX':'O',
  'IMAX2':'',
  'IMAX3':'',
  'PMAX':'N',
  'PAPP':'O',
  'HHPHC':'0',
  'MOTDETAT':'0',
  'PPOT':'N'}



class Teleinfo_serial:

        ser = serial.Serial()

        def __init__ (self, port='/dev/ttyUSB0'):
                try:
                  self.port=port
                  self.ser = serial.Serial()
                  self.validate=None
                except OSError as e:
                  logging.critical('Could not open serial port : %s',e)
                  sys.exit(1)

                try:
                  self.ser.baudrate = 1200
                  self.ser.port = port
                  self.ser.parity = serial.PARITY_EVEN
                  self.ser.bytesize = serial.SEVENBITS

                  if self.ser.isOpen():
                    self.ser.close()
                  self.ser.open()
                except OSError as e:
                  logging.critical('Could not open serial port : %s',e)
                  sys.exit(1)
                except serial.serialutil.SerialException:
                  logging.critical('Cannot settings serial port %s',self.port)
                  sys.exit(1)

                time.sleep(1)


        def set_mode (self, mode):
          if mode=='TEMPO':
            self.validate=TEMPO_TI


        def checksum (self, etiquette, valeur):
                sum = 32
                for c in etiquette: sum = sum + ord(c)
                for c in valeur:        sum = sum + ord(c)
                sum = (sum & 63) + 32
                #print('checksum of %s %s is %c' %(etiquette,valeur,sum))
                return chr(sum)

        def read (self,framesOK):
          # clear serial buffer to provide current meter data
          try:
            self.ser.flushInput()
          except serial.serialutil.SerialException:
            logging.critical('Cannot flush serial port %s',self.port)
            sys.exit(1)

          brk=6
          while 'O' in self.validate.values():
            brk-=1
            if brk<0:
              break

            # Wait for data
            while self.ser.read(1) != chr(2):
              pass

            message = ""
            completed = False
            while not completed:
              char = self.ser.read(1)
              if char != chr(2):
                message = message + char
              else:
                completed = True

            frames = [ filter(None,frame.split(" ")) for frame in message.strip("\r\n\x03").split("\r\n")]
            for frame in frames:
              if( ((len(frame) == 3) and (self.checksum(frame[0],frame[1]) == frame[2])) or (len(frame) == 2)):
                framesOK[frame[0]] = frame[1]
                if frame[0] in self.validate:
                  del self.validate[frame[0]]
              else:
                print('invalid checksum frame %s' %(frame[0]))


            time.sleep(0.3)
          return framesOK

        def test(self,framesOK):
          message='''
ADCO 700609361116 ?\r
OPTARIF BBR( S\r
ISOUSC 20 8\r
BBRHCJB 001444126 3\r
BBRHPJB 001228815 E\r
BBRHCJW 005444126 L\r
BBRHPJW 005228815 ^\r
BBRHCJR 002444126 D\r
BBRHPJR 002228815 V\r
PTEC HP D\r
IINST1 002 J\r
IMAX1 011 2\r
PMAX 07470 8\r
PAPP 00610 (\r
DEMAIN ROUG +\r
'''
          brk=2
          while 'O' in self.validate.values():
            brk-=1
            if brk<0:
              break
            print('----------------')
            print('###  brk  %d ###' % brk)
            frames = [ frame.split(" ") for frame in message.strip("\r\n\x03").split("\r\n")]

            for frame in frames:
              if (len(frame) == 3) and (self.checksum(frame[0],frame[1]) == frame[2]):
                framesOK[frame[0]] = frame[1]
                if frame[0]in self.validate:
                  del self.validate[frame[0]]
              else:
                print('invalid checksum for frame %s' %(frame[0]))

            for k,frame in framesOK.items():
              print("%s : %s" %(k,frame))
            print('----------------\n')

            time.sleep(0.3)

          print(framesOK.values())

          return framesOK
        def close (self):
          self.ser.close()


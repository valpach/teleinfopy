#!/home/teleinfo/.virtualenvs/teleinfopy/bin/python2
# -*- coding: utf-8 -*-

import begin
import logging
import time
import sdnotify
import datetime
try:
  import RPi.GPIO as GPIO
except RuntimeError:
 print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


from teleinfo.teleinfo_serial import Teleinfo_serial
import paho.mqtt.client as mqtt

framesHCTI={
  'HCHC':'O',
  'HCHP':'O',
  'IINST':'O',
  'IMAX':'O',
  'PAPP':'O'}


def mqtt_publish(ti,mqtt_host, mqtt_user, mqtt_password, mqtt_port):
  client = mqtt.Client()
  client.username_pw_set(mqtt_user, password=mqtt_password)

  client.connect(mqtt_host, mqtt_port, 60)
  client.loop_start()
  papp=int(ti['PAPP'])
  if papp < 20000 and papp >= 0:
    logging.info("PAPP {0}".format(papp))
    client.publish('teleinfo/PAPP', papp)

  hc=str(int(ti['HCHC']))
  client.publish('teleinfo/HC', hc[:5])
  hp=str(int(ti['HCHP']))
  client.publish('teleinfo/HP', hp[:5])
  iinst=str(int(ti['IINST']))
  client.publish('teleinfo/IINST', iinst)
  imax=str(int(ti['IMAX']))
  client.publish('teleinfo/IMAX', imax)

  client.publish('teleinfo/Time', datetime.datetime.now().isoformat())

  time.sleep(1)

  client.loop_stop()
  client.disconnect()


@begin.start(config_file='/etc/teleinfo.cfg')
@begin.logging
def default(device='/dev/ttyAMA0',
            mode='mqtt',
            mqtt_host='localhost',
            mqtt_user='user',
            mqtt_password='password',
            mqtt_port=1883,
            led_gpio=7):
  logging.info("device : %s",device)
  logging.info("led : %s",led_gpio)
  serial_device=Teleinfo_serial(port=device)
  n = sdnotify.SystemdNotifier()
  n.notify("READY=1")
  if led > 0 :
    GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
    GPIO.setwarnings(False)    # Ignore warning for now
    GPIO.setup(led,GPIO.OUT)

  try:
    while True:
      n.notify("WATCHDOG=1")
      time.sleep(2)
      data=serial_device.read(framesHCTI)
      if data is False:
        continue
      if led_gpio > 0 :
        GPIO.output(led,GPIO.HIGH)
      if mode == 'mqtt':
        mqtt_publish(data,mqtt_host, mqtt_user, mqtt_password, mqtt_port)
      if led_gpio > 0 :
        time.sleep(0.8)
        GPIO.output(led,GPIO.LOW)
      time.sleep(15)
  except KeyboardInterrupt:
    pass
  serial_device.close()
  GPIO.output(led,GPIO.LOW)



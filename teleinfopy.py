#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
import begin
import logging

from teleinfo.teleinfo_serial import Teleinfo_serial
import paho.mqtt.client as mqtt



framesTI={
  'ADCO':'',
  'OPTARIF':'',
  'ISOUSC':'',
  'BASE':'',
  'HCHC':'0',
  'HCHP':'0',
  'EJPHN':'0',
  'EJPHPM':'0',
  'BBRHCJB':'0',
  'BBRHPJB':'0',
  'BBRHCJW':'0',
  'BBRHPJW':'0',
  'BBRHCJR':'0',
  'BBRHPJR':'0',
  'PEJP':'0',
  'PTEC':'',
  'DEMAIN':'',
  'IINST':'0',
  'IINST1':'0',
  'IINST2':'0',
  'IINST3':'0',
  'IMAX':'0',
  'IMAX1':'0',
  'IMAX2':'0',
  'IMAX3':'0',
  'PMAX':'0',
  'PAPP':'',
  'HHPHC':'',
  'MOTDETAT':'',
  'PPOT':''}


def mqtt_publish(ti,mqtt_host, mqtt_user, mqtt_password, mqtt_port):
  client = mqtt.Client()
  client.username_pw_set(mqtt_user, password=mqtt_password)

  client.connect(mqtt_host, mqtt_port, 60)
  client.loop_start()
  client.publish('teleinfo/PAPP', int(ti['PAPP']))
  hc=str(int(ti['HCHC']))
  hp=str(int(ti['HCHP']))
  client.publish('teleinfo/HC', hc[:5])
  client.publish('teleinfo/HP', hp[:5])
  client.disconnect()


@begin.start(config_file='teleinfo.cfg')
@begin.logging
def default(device='/dev/ttyAMA0',mode='mqtt',mqtt_host, mqtt_user, mqtt_password, mqtt_port):
  logging.info("device : %s",device)
  serial_device=Teleinfo_serial(port=device)
  serial_device.set_mode('TEMPO')
  data=serial_device.read(framesTI)
  if mode == 'mqtt':
    mqtt_publish(data,mqtt_host, mqtt_user, mqtt_password, mqtt_port)
  logging.info("insertion des données")



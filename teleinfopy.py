#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
import begin
import logging
import _mysql

from teleinfo.teleinfo_serial import Teleinfo_serial



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


#-------------------------------------------------------------
# Insertion d'un jeu de mesure dans la base mySQL
#-------------------------------------------------------------
def insertTeleinfoMySQL(ti,host,user,password,database,table) :

  if(type(ti)!=dict):
    logging.error("Format des données invalides")
    sys.exit(1)
  placeholders = ', '.join(['%s'] * len(ti))
  columns = ', '.join(ti.keys())
  sql = "INSERT INTO %s (%s) VALUES (%s)" % (table,columns,placeholders)

  try:
    con = _mysql.connect(
         host=host,
         user=user,
         passwd=password,
         db=database)
  except MySQLdb.Error as e:
    logging.error("[connectMySQL] Error [%d]: %s" % (e.args[0], e.args[1]))
    sys.exit(1)
  cursor = con.cursor()

  try :
    # On insere dans la base
    cursor.execute(sql,ti.values())
    con.commit()
  except MySQLdb.Error as e:
    con.rollback()
    logging.error("%s",e)
  con.close()


@begin.start(config_file='teleinfo.cfg')
@begin.logging
def default(device='/dev/ttyAMA0',db_host='localhost',db_user='root',db_password='root',db_database='teleinfo',db_table='DbiTeleinfo'):
  logging.info("device : %s",device)
  serial_device=Teleinfo_serial(port=device)
  serial_device.set_mode('TEMPO')
  data=serial_device.read(framesTI)
  insertTeleinfoMySQL(data,db_host,db_user,db_password,db_database,db_table)
  logging.info("insertion des données")







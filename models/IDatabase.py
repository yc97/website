#!/usr/bin/python
#encoding:utf-8

"""
File name:    Database.py
Author:       hjx
Date:         2015年7月23日
Description:  Database
"""
import ConfigParser
from decimal import Decimal
class Defaults:
    '''A collection of database default values
    '''
    config_path = './config/data.conf'
    config_path_in = '../config/data.conf'
    dbName = 'db'#data.conf里的[db]
    database = 'Fac'
    cf = ConfigParser.ConfigParser()
    if cf.read(config_path) == []:
        cf.read(config_path_in)
    demForm = cf.get('config', 'demForm')

    def changeForm(self, num):
        return float(Decimal(num).quantize(Decimal(self.demForm)))

class Database(object):
    def __init__(self):
        pass








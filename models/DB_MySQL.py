#encoding:utf-8
#!/usr/bin/python
__author__ = 'stevewong'

import MySQLdb
import sys
import datetime
import ConfigParser

from IDatabase import Database
from IDatabase import Defaults

class MySQLDatabase(Database):
    '''Implementation of MySQL
    '''
    def __init__(self, dbName = Defaults.dbName, database = Defaults.database):
        #调用config文件来初始化数据库参数（host,database,user,passwd,port）并连接数据库
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(Defaults.config_path)
            #print read
            self.host = cf.get(dbName, 'db_host')
            self.database = database
            self.user = cf.get(dbName, 'db_user')
            self.passwd = cf.get(dbName, 'db_passwd')
            self.port = cf.get(dbName, 'db_port')
            super(MySQLDatabase, self).__init__()

            #打开数据库连接
            #print self.host, self.user, self.passwd, self.database, int(self.port)
            self.db = MySQLdb.connect(self.host, self.user, self.passwd, self.database, int(self.port))
            #print self.db
            #使用cursor()方法获取操作游标
            self.db.set_character_set('utf8')
            self.cursor = self.db.cursor()
            self.cursorDict = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.db.autocommit(1)#自动提交
        except:
            print 'error: Database __init__ ', sys.exc_info()[1]

    def execute(self, cmd):
        try:
            replyNum = self.cursor.execute(cmd)
            if replyNum == 0:#执行语句错误，定义错误代码为2
                return {'code': 2,
                        'info': 'Error! From MySQLDatabase.execute: No record or execute failed',
                        'cmd': cmd}
            record = self.cursor.fetchall()
            #执行成功的代码为0
            return {'code': 0, 'replyNum': replyNum, 'result': record}
        except MySQLdb.Error, e:
            #其他错误，错误代码为1
            return {'code': 1, 'info': "Mysql Error %d! from execute(): %s" % (e.args[0], e.args[1]), 'cmd': cmd}

    def executeDict(self, cmd):
        #返回字典
        try:
            replyNum = self.cursorDict.execute(cmd)
            if replyNum == 0:#执行语句错误，定义错误代码为2
                return {'code': 2,
                        'info': 'Error! From MySQLDatabase.execute: No record or execute failed',
                        'cmd': cmd}
            record = self.cursorDict.fetchall()
            #执行成功的代码为0
            return {'code': 0, 'replyNum': replyNum, 'result': record}
        except MySQLdb.Error, e:
            #其他错误，错误代码为1
            return {'code': 1, 'info': "Mysql Error %d! from executeDict(): %s" % (e.args[0], e.args[1]), 'cmd': cmd}

    def close(self):
        self.db.close()
        return

if __name__ == '__main__':
    Defaults.config_path = '../config/data.conf'



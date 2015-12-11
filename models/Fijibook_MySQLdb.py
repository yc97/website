#encoding:utf-8
#!/usr/bin/python
__author__ = 'stevewong'

from DB_MySQL import MySQLDatabase
from IDatabase import Defaults
import traceback

class Fijibook_MySQLdb(MySQLDatabase):
    def __init__(self):
        try:
            super(Fijibook_MySQLdb, self).__init__(dbName='MySQL', database='fijibook')
        except Exception as e:
            print traceback.format_exc()

    def getBalance(self, user):
        usertable = 'balance'
        cmd = "select money from %s where user = '%s' " % (usertable, user)
        return self.execute(cmd)

    def saveBalance(self, user, money, location='', remark='', type='', lng='', lat=''):
        usertable = 'balance'
        cmd1 = "insert into %s (`user`, `money`, `time`, `location`, `remark`, `type`, `lng`, `lat`) \
                values('%s', %f, now(), '%s', '%s', '%s', '%s', '%s')" \
               % (usertable, user, float(money), location, remark, type, lng, lat)
        rec = self.execute(cmd1)
        self.db.commit()
        return rec

    def addUser(self, user, password):
        try:
            cmd0 = "select * from User where user = '%s'" % (user)
            rec0 = self.execute(cmd0)
            if rec0['code'] == 0:#成功执行，说明记录已存在
                return {'code': 3, 'info': 'Error! User exists!'}
            elif rec0['code'] == 2:
                #记录不存在，可以插入
                cmd1 = """INSERT INTO User(user, passwd)\
                        VALUES('%s', md5('%s')) """\
                                % (user, password)
                #print cmd1
                rec1 = self.execute(cmd1)
                #print rec1
                if not rec1['code']:#成功执行
                    return {'code': 0, 'info': 'Insert user OK!'}
                else:
                    return rec1
            else:#code==1,其他错误
                return rec0
        except Exception as e:
            return {'code': 1, 'info': 'Error! from AddUser: ' + e.message}

    def delUser(self, user):
        try:
            cmd = "delete from User \
                where user = '%s'" % (user)
            dict_res = self.execute(cmd)
            #print dict_res
            if dict_res['code'] == 2:#执行失败,说明记录不存在
                return {'code': 2, 'info': 'User not exist!'}
            elif dict_res['code'] == 0:#执行成功
                return {'code': 0, 'info': 'Delete user OK!'}
            return dict_res
        except Exception as e:
            return {'code': 1, 'info': 'Error! from delUser: ' + e.message}

    def login(self, user, password):
        try:
            cmd = "select user, passwd from User \
                where user = '%s' and passwd = md5('%s')" % (user, password)
            rec = self.execute(cmd)
            if not rec['code']:
                return {'code': 0, 'info': 'Login OK!', 'user': rec['result'][0][0]}
            else:
                return rec
        except Exception as e:
            return {'code': 1, 'info': 'Error! from login: ' + e.message}

    def getUserSum(self):
        cmd = "select count(*) from `User`"
        return self.execute(cmd)

    def getRecSum(self):
        usertable = 'balance'
        cmd = "select count(*) from %s"% usertable
        return self.execute(cmd)

    def getUserRecSum(self, user):
        usertable = 'balance'
        cmd = "select count(*) from %s where user = '%s'"% (usertable, user)
        return self.execute(cmd)

    def getNewestRecTime(self, user):
        usertable = 'balance'
        cmd = "select max(time) from %s where `user` = '%s'"% (usertable, user)
        return self.execute(cmd)

    def getTable(self):
        usertable = 'balance'
        cmd = "select `user`, `money`, `time`, `location`, `remark`, `type` from %s where `user` = '%s'" % (usertable, user)
        return self.execute(cmd)

    def getUserTable(self, user):
        usertable = 'balance'
        cmd = "select `user`, `money`, `time`, `location`, `remark`, `type` from %s where `user` = '%s'" % (usertable, user)
        return self.execute(cmd)

    # def createUserTable(self, user):
    #     usertable = user + '_balance'
    #     cmd = "create table %s like balance" % str(usertable)
    #     return self.execute(cmd)
    def getExpenseTypes(self, user):
        cmd = "select `subtype` from type where user in ('all','%s') and inex='expenses'" % (user)
        return self.execute(cmd)

    def getIncomeTypes(self, user):
        cmd = "select `subtype` from type where user in ('all','%s') and inex='income'" % (user)
        return self.execute(cmd)

if __name__ == '__main__':
    Defaults.config_path = '../config/data.conf'
    print Fijibook_MySQLdb().addUser('luke', 'jmb12e')



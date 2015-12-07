#!/usr/bin/python
#encoding:utf-8
import tornado.web
import traceback
from models.Fijibook_MySQLdb import Fijibook_MySQLdb
from handlers.BaseHandler import BaseHandler

class indexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #print 'index'
        user = self.get_current_user()
        recSumRec = Fijibook_MySQLdb().getUserRecSum(user)
        userSumRec = Fijibook_MySQLdb().getUserSum()
        newTimeRec = Fijibook_MySQLdb().getNewestRecTime(user)
        tableRec = Fijibook_MySQLdb().getUserTable(user)
        # tableRec = Fijibook_MySQLdb().getTable()
        if recSumRec['code'] or userSumRec['code'] or newTimeRec['code'] or tableRec['code']:
            self.render('index.html', user=user, recSum=-1,
                        userSum=-1, newTime=-1,
                        thead=['user', 'money', 'time', 'location', 'usage', 'usageType'],
                        tbody=[])
            print('Error getting recSum or userSum or newTime or table. \
            code : [recSum, userSum, newTime, table]'
                       + str(recSumRec) + str(userSumRec) + str(newTimeRec) + str(tableRec))
        else:
            self.render('index.html', user=user, recSum=recSumRec['result'][0][0],
                        userSum=userSumRec['result'][0][0], newTime=newTimeRec['result'][0][0],
                        thead=['user', 'money', 'time', 'location', 'usage', 'usageType'],
                        tbody=tableRec['result'])

    @tornado.web.authenticated
    def post(self):
        user = self.get_secure_cookie('user')
        money = self.get_argument('money')
        location = self.get_argument('inputLocation')
        usage = self.get_argument('usage')
        usageType = self.get_argument('usageType')
        lng = self.get_argument('lng')
        lat = self.get_argument('lat')
        rec = Fijibook_MySQLdb().saveBalance(user=user, money=money, location=location, usage=usage, usageType=usageType, lng=lng, lat=lat)
        if rec['code']:
            self.write(rec)
        self.redirect('/index')
        # bikeSumRec = Fijibook_MySQLdb().getRecSum()
        # userSumRec = Fijibook_MySQLdb().getUserSum()
        # newTimeRec = Fijibook_MySQLdb().getNewestRecTime()
        # tableRec = Fijibook_MySQLdb().getTable()
        # if bikeSumRec['code'] or userSumRec['code'] or newTimeRec['code'] or tableRec['code']:
        #     self.write('Error getting bikeSum or userSum or newTime or table')
        # else:
        #     self.render('index.html', user=user, bikeSum=bikeSumRec['result'][0][0],
        #                 userSum=userSumRec['result'][0][0], newTime=newTimeRec['result'][0][0],
        #                 thead=['bikeNO', 'passwd', 'addTime', 'user'],
        #                 tbody=tableRec['result'])

# class passwdHandler(BaseHandler):
#     @tornado.web.authenticated
#     def post(self):
#         bikeNO = self.get_argument('bikeNO')
#         rec = Fijibook_MySQLdb().getBalance(bikeNO)
#         if rec['code'] == 0:
#             passwd = rec['result'][0][0]
#             self.render('showPasswd.html', bikeNO=bikeNO, password=passwd)
#         elif rec['code'] == 2:
#             self.render('inputPasswd.html', bikeNO=bikeNO)
#         else:
#             self.write('Error. Sorry.')

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', info='')

    def post(self):
        user = self.get_argument('user')
        passwd = self.get_argument('passwd')
        rec = Fijibook_MySQLdb().login(user, passwd)
        #print rec
        if rec['code'] == 0:
            self.set_secure_cookie("user", user)
            #self.set_secure_cookie("passwd", passwd, expires_days=None)
            self.redirect('/index')

        else:
            self.render('login.html', info='Unmatched user and password, please try again.')

class registerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html', info='')

    def post(self):
        user = self.get_argument('user')
        passwd = self.get_argument('passwd')
        rec = Fijibook_MySQLdb().addUser(user, passwd)
        #print rec
        if rec['code'] == 0:
            self.set_secure_cookie("user", user)
            #self.set_secure_cookie("passwd", passwd, expires_days=None)
            res = Fijibook_MySQLdb().createUserTable(user)
            if not res['code']:
                print("Error creating '%s' table!"%user)
            self.redirect('/login')
        else:
            self.render('register.html', info='Unknown error!.')


class LogoutHandler(BaseHandler):
    def get(self):
        #print self.get_argument("logout", None)
        self.clear_cookie("user")
        self.redirect("/index")
        #if (self.get_argument("logout", None)):


class MapHandler(BaseHandler):
    def get(self):
        self.render('map.html')

class JSMapHandler(BaseHandler):
    def get(self):
        self.render('map1.html')
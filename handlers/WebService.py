#!/usr/bin/python
#encoding:utf-8
import tornado.web
import traceback
from models.Fijibook_MySQLdb import Fijibook_MySQLdb
from handlers.BaseHandler import BaseHandler
from VerificationCode import VerificationCode
import StringIO
import datetime
import sys
import json

class indexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #print 'index'
        user = self.get_current_user()
        print user, 'login at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sys.stdout.flush()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        recSumRec = Fijibook_MySQLdb().getUserRecSum(user)
        userSumRec = Fijibook_MySQLdb().getUserSum()
        newTimeRec = Fijibook_MySQLdb().getNewestRecTime(user)
        tableRec = Fijibook_MySQLdb().getRecord(user, today)
        expenseTypesRec = Fijibook_MySQLdb().getExpenseTypes(user)
        incomeTypesRec = Fijibook_MySQLdb().getIncomeTypes(user)
        # tableRec = Fijibook_MySQLdb().getTable()
        if recSumRec['code'] or userSumRec['code'] or newTimeRec['code'] or expenseTypesRec['code'] or incomeTypesRec['code']:
            self.render('bootstrap_test.html', user=user, recSum=0,
                        userSum=-1, newTime=-1,
                        thead=['时间', '位置', '金额',  '账单分类', '备注'],today=today,
                        tbody=[], expensebody=expenseTypesRec['result'], incomebody=incomeTypesRec['result'])
            print('Table is empty. Or error getting recSum or userSum or newTime or table. \
            code : [recSum, userSum, newTime, table, types]'
                       + str(recSumRec) + str(userSumRec) + str(newTimeRec) + str(tableRec) + str(expenseTypesRec) + str(incomeTypesRec))
        else:
            try:
                tbody = tableRec['result']
            except KeyError:
                tbody = (('No record. Please add ', ' ', ' ', ' ', ' '), (' ', ' ', ' ', ' ', ' '))
            self.render('bootstrap_test.html', user=user, recSum=recSumRec['result'][0][0],
                        userSum=userSumRec['result'][0][0], newTime=newTimeRec['result'][0][0],
                        today=today,
                        thead=['时间', '位置', '金额',  '账单分类', '备注'],
                        tbody=tbody,
                        expensebody=expenseTypesRec['result'],
                        incomebody=incomeTypesRec['result'])

    @tornado.web.authenticated
    def post(self):
        user = self.get_secure_cookie('user')
        money = self.get_argument('money')
        location = self.get_argument('inputLocation')
        remark = self.get_argument('remark')
        type = self.get_argument('type')
        moneySel = self.get_argument('moneySel')
        if moneySel == 'expenses':
            money = -float(money)
        lng = self.get_argument('lng')
        lat = self.get_argument('lat')
        rec = Fijibook_MySQLdb().saveBalance(user=user, money=money, location=location, remark=remark, type=type, lng=lng, lat=lat)
        if rec['code']:
            self.write(rec)
        self.redirect('/index')

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
        self.render('register.html', info='', isCorrect='')

    def post(self):
        user = self.get_argument('user')
        passwd = self.get_argument('passwd')
        verificationCode = self.get_argument('verificationCode')
        correctCode = self.get_secure_cookie("verificationCode")
        #print correctCode,verificationCode
        if verificationCode.upper() != correctCode.upper():
            self.render('register.html', info='', isCorrect='wrong verification code')
        else:
            rec = Fijibook_MySQLdb().addUser(user, passwd)
            #print rec
            if rec['code'] == 0:
                self.set_secure_cookie("user", user)
                #self.set_secure_cookie("passwd", passwd, expires_days=None)
                # res = Fijibook_MySQLdb().createUserTable(user)
                # if not res['code']:
                #     print("Error creating '%s' table!"%user)
                self.redirect('/index')
            else:
                self.render('register.html', info='Unknown error!.', isCorrect='')

class VerificationImgHandler(BaseHandler):
    def get(self):
        #get img
        image, code = VerificationCode().createImg()
        #save code to cookie
        self.set_secure_cookie("verificationCode", code)
        #save to stringio
        msstream = StringIO.StringIO()
        image.save(msstream, 'jpeg')
        #get data from stringio
        img_data = msstream.getvalue()
        msstream.close()
        #set content type
        self.set_header('Content-type', 'image/jpg')
        self.set_header('Content-length', len(img_data))
        #response write
        self.write(img_data)

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


class POIHandler(BaseHandler):
    def get(self):
        self.render('POI.html')

class RecordHandler(BaseHandler):
    def get(self):
        mydate = self.get_argument('myDate')
        user = self.get_current_user()
        #print mydate, user
        recordRec = Fijibook_MySQLdb().getRecord(user, mydate)
        try:
            record = recordRec['result']
        except KeyError:
            record = (('No record. Please add ', ' ', ' ', ' ', ' '), (' ', ' ', ' ', ' ', ' '))
        recordJson = json.dumps(record)
        self.write(recordJson)

    def post(self):
        user = self.get_current_user()
        time = self.get_argument('time')
        money = self.get_argument('money')
        money = float(money)
        remark = self.get_argument('remark')
        type = self.get_argument('type')
        moneySel = self.get_argument('moneySel')
        #print user, time, money, remark, type, moneySel
        if moneySel == 'expenses':
            money = -(money)
        res = Fijibook_MySQLdb().updateRecord(user, time, money, remark, type)
        #if res['code']:
            #print 'update record failed!'

    def delete(self):
        user = self.get_current_user()
        time = self.get_argument('time')
        #print user, time
        res = Fijibook_MySQLdb().delRecord(user, time)
        if res['code']:
            self.write('delete record failed!')
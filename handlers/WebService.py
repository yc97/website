# !/usr/bin/python
# encoding:utf-8
import tornado.web
# import traceback
from models.Website_MySQLdb import Website_MySQLdb
from handlers.BaseHandler import BaseHandler
from VerificationCode import VerificationCode
import StringIO
import datetime
import sys
import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
class FunctionsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        print user, 'login at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sys.stdout.flush()
        self.render('Functions.html', user=user)
class systemHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        sys.stdout.flush()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.render('system_management.html', user=user)
class healthHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # print 'index'
        user = self.get_current_user()
        sys.stdout.flush()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        recSumRec = Website_MySQLdb().getUserRecSum(user)
        tableRec = Website_MySQLdb().getRecord(user, today)
        if recSumRec['code']:
            self.render('health.html', user=user, recSum=0,today=today,tbody=[],
                        thead=['时间', '产品名称', '产品编号',  '特征参数', '维修提示', '维修指导', '备注'])
            # print('Table is empty. Or error. ')
        else:
            try:
                tbody = tableRec['result']
            except KeyError:
                tbody = (('No record. Please add ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '), (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
            self.render('health.html', user=user, recSum=recSumRec['result'][0][0],today=today,tbody=tbody,
                        thead=['用户','时间', '产品名称', '产品编号',  '特征参数',  '维修提示', '维修指导', '开始时间', '周期', '备注'])
    @tornado.web.authenticated
    def post(self):
        user = self.get_secure_cookie('user')
        number = self.get_argument('number')
        name = self.get_argument('prName')
        remark = self.get_argument('remark')
        myType = self.get_argument('type')
        dateStart = self.get_argument('dateStart')
        period = self.get_argument('period')
        tips = self.get_argument('tips')
        guide = self.get_argument('guide')
        rec = Website_MySQLdb().saveMaintain(user=user, NO=number, name=name, remark=remark, PRM=myType, tips=tips, guide=guide, start=dateStart, period=period)
        if rec['code']:
            self.write(rec)
        self.redirect('/health')
class historyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        sys.stdout.flush()
        self.render('history.html', user=user, today = today)

class indexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # print 'index'
        user = self.get_current_user()
        print user, 'login at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sys.stdout.flush()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        recSumRec = Website_MySQLdb().getUserRecSum(user)
        tableRec = Website_MySQLdb().getRecord(user, today)
        if recSumRec['code']:
            self.render('index.html', user=user, recSum=0,today=today,tbody=[],
                        thead=['时间', '产品名称', '产品编号',  '特征参数', '维修提示', '维修指导', '备注'])
            # print('Table is empty. Or error. ')
        else:
            try:
                tbody = tableRec['result']
            except KeyError:
                tbody = (('No record. Please add ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '), (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
            self.render('index.html', user=user, recSum=recSumRec['result'][0][0],today=today,tbody=tbody,
                        thead=['用户','时间', '产品名称', '产品编号',  '特征参数',  '维修提示', '维修指导', '开始时间', '周期', '备注'])
    @tornado.web.authenticated
    def post(self):
        user = self.get_secure_cookie('user')
        number = self.get_argument('number')
        name = self.get_argument('prName')
        remark = self.get_argument('remark')
        myType = self.get_argument('type')
        dateStart = self.get_argument('dateStart')
        period = self.get_argument('period')
        tips = self.get_argument('tips')
        guide = self.get_argument('guide')
        rec = Website_MySQLdb().saveMaintain(user=user, NO=number, name=name, remark=remark, PRM=myType, tips=tips, guide=guide, start=dateStart, period=period)
        if rec['code']:
            self.write(rec)
        self.redirect('/index')

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html', info='')

    def post(self):
        user = self.get_argument('user')
        passwd = self.get_argument('passwd')
        rec = Website_MySQLdb().login(user, passwd)
        #print rec
        if rec['code'] == 0:
            self.set_secure_cookie("user", user)
            #self.set_secure_cookie("passwd", passwd, expires_days=None)
            self.redirect('/Functions')
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
            rec = Website_MySQLdb().addUser(user, passwd)
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

class RecordHandler(BaseHandler):
    def get(self):
        mydate = self.get_argument('myDate')
        user = self.get_current_user()
        #print mydate, user
        recordRec = Website_MySQLdb().getRecord(user, mydate)
        try:
            record = recordRec['result']
        except KeyError:
            record = (('No record. Please add ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '), (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
        recordJson = json.dumps(record)
        self.write(recordJson)

    def post(self):
        user = self.get_current_user()
        time = self.get_argument('time')
        name = self.get_argument('name')
        NO = self.get_argument('NO')
        prm = self.get_argument('prm')
        tips = self.get_argument('tips')
        guide = self.get_argument('guide')
        timeStart = self.get_argument('timeStart')
        period = self.get_argument('period')
        detail = self.get_argument('detail')
        #print user, time, money, remark, type, moneySel

        res = Website_MySQLdb().updateRecord(user, time, name, NO, prm, tips, guide, timeStart, period, detail)
        #if res['code']:
            #print 'update record failed!'

    def delete(self):
        user = self.get_current_user()
        time = self.get_argument('time')
        #print user, time
        res = Website_MySQLdb().delRecord(user, time)
        if res['code']:
            self.write('delete record failed!')

class SetupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        allSys = Website_MySQLdb().GetSys(user)
        if allSys['code']:
            self.write({'status': '0', 'result': 'Get systems failed!'})
        else:
            self.write({'status': '1', 'result': allSys['result']})
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        source = self.get_argument('source')
        isUpdate = self.get_argument('isUpdate')
        print isUpdate
        # get option from source
        if source == 'file':
            optionFile = self.request.files['file']
            treeOption = optionFile[0]['body']
        elif source == 'json':
            treeOption = self.get_argument('treeOption')
        else:
            self.write({'state': 'Cant get options!'});
            return
        optionJson = eval(treeOption)
        # print optionJson[0]['id']
        # get sysName
        if optionJson[0]['id'] == 'root':
            sysName = optionJson[0]['text']
        else:
            for option in optionJson:
                if option['id'] == 'root':
                    sysName = optionJson[0]['text']
        if isUpdate == 1:
            res = Website_MySQLdb().UpdateSys(user=user, sysName=sysName, treeOption=treeOption)
            if res['code'] == 1:
                self.write({'state': 'Update system options failed!'})
            else:
                self.write({'state': 'Update system options successful!'})
        else:
            print sysName,treeOption
            res = Website_MySQLdb().SaveSys(user=user, sysName=sysName, treeOption=treeOption)
            if res['code'] == 1:
                self.write({'code': 0, 'state': 'Save system options failed!'})
            elif res['code'] == -1:
                self.write({'code': -1, 'state': 'This system exists!'})
            else:
                self.write({'code': 1, 'state': 'Save system options successful!'})

class FilesHandler(BaseHandler):
     def post(self):
        user = self.get_current_user()
        userId = Website_MySQLdb().getUserId(user)['result'][0][0]
        # 提取表单中‘name’为‘file’的文件元数据
        myFile = self.request.files['file']
        # fileName=myFile[0]['filename']
        upload_path = os.path.join(os.path.dirname(__file__), os.pardir, 'users', str(userId))  # 文件的暂存路径
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        # print upload_path
        for meta in myFile:
            filename = 'myfile.csv'
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:      # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
                self.write({'status': '上传成功'})

     def get(self):
        user = self.get_current_user()
        userId = Website_MySQLdb().getUserId(user)
        fileName = self.get_argument('filename')
        # print fileName
        if not userId['code']:
            filePath=os.path.join(os.path.dirname(__file__), os.pardir, 'users', str(userId['result'][0][0]), fileName)  #头像文件路径
            try:
                with open(filePath, 'rb') as f:
                    fileData = f.read()
            except:
                pass
        list = fileData.split('\r\n')
        fieldsName = list.pop(0).split(',')
        myFile = []
        for item in list:
            item = item.split(',')
            if len(item) == len(fieldsName):
                # print item
                row = {}
                for i in range(len(fieldsName)):
                    row[fieldsName[i]] = item[i]
                    # print item[i]
                myFile.append(row)
        # print myFileJson
        myFileJson = json.dumps(myFile)
        self.write(myFileJson)
#!/usr/bin/python
#encoding:utf-8

## Copyright (C), 2015-2017, ****.
## project name:    pgx_WebService
## Author:          hjx
## Version:         0.2
## Date:            2015-07-24
## Description:
## History:         0.2
##   1. Date:
##      Author:    hjx
##      Modification:
##   2. ...


from handlers.WebService import indexHandler, loginHandler, LogoutHandler, MapHandler, \
    JSMapHandler, registerHandler, POIHandler

from handlers.WebService import indexHandler, loginHandler, LogoutHandler, MapHandler, JSMapHandler, registerHandler, VerificationImgHandler


urls = [
    ('/', indexHandler),
    ('/login', loginHandler),
    ('/logout', LogoutHandler),
    ('/index', indexHandler),
    ('/register', registerHandler),
    ('/map', MapHandler),
    ('/jsmap', JSMapHandler),
    ('/poi', POIHandler),
    ('/register', registerHandler),
    ('/verificationimg', VerificationImgHandler),
    ]


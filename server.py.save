#!/usr/bin/python
#encoding:utf-8

## Copyright (C), 2015-2017, ****.
## project name:    pxg
## Author:          hjx
## Version:         0.2
## Date:            2015-07-24
## Description:     
## History:         0.2
##   1. Date:
##      Author:    hjx
##      Modification:
##   2. ...


import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import setting
import os.path

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkH054adsXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "login_url": "/login"
    }
    application = tornado.web.Application(
        handlers=setting.urls,
        debug=True,
        **settings
        )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

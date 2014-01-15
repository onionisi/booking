# coding=utf-8
import uuid
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from pymongo import MongoClient
from tornado.options import define, options

import tempfile
import time
import logging
from pgmagick import Image

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", HomeHandler),
                (r"/class", ClassHandler),
                (r"/register", RegHandler),
                (r"/login", LoginHandler),
                (r"/logout", LogoutHandler),
                (r"/mine", MineHandler),
                (r"/cart", CartHandler),
                (r"/c_show", Cshow_Handler),
                (r"/admin", Admin_Handler),
                ]
        settings = dict(
                title = u"NAME",
                template_path = os.path.join(os.path.dirname(__file__), "templates"),
                static_path = os.path.join(os.path.dirname(__file__), "static"),
                ui_modules = {"Unit": UnitModule},
                #xsrf_cookies = True,
                cookie_secret = uuid.uuid4(),
                debug = True,
                )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = MongoClient('localhost', 27017).test

class UnitModule(tornado.web.UIModule):
    def render(self, each):
        return self.render_string("modules/good.html", each=each)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("admin")
        if not user_id: return None
        return None

class HomeHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class ClassHandler(BaseHandler):
    def get(self):
        self.render("class.html")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("ln")
        message = {}
        message['errno'] = 0

        self.write(message)

class MineHandler(BaseHandler):
    pass

class CartHandler(BaseHandler):
    pass

class Cshow_Handler(BaseHandler):
    def get(self):
        class_id = self.get_argument("class_id")
        entry = self.db.goods.find()
        self.render("c_show.html", entry=entry)

class LoginHandler(BaseHandler):
    def get(self):
        referer = self.request.headers.get("Referer")
        self.render("login.html", referer=referer)

    def post(self):

        args = self.request.arguments
        name = self.get_argument("login_name")
        passwd = self.get_argument("password")

        customer = {"name": name,
                    "passwd": passwd}
        phone = {"phone": name,
                    "passwd": passwd}
        message = {}

        if self.db.users.find_one(customer) or\
                self.db.users.find_one(phone):
            self.set_cookie("ln", name)
            message['errno'] = 0
            message['msg'] = u"欢迎光临"
        else:
            message['errno'] = 1
            message['msg'] = u"帐号或者密码不正确"

        self.write(message)

class Admin_Handler(BaseHandler):
    def get(self):
        self.render("upload.html")

    def post(self, obj=None):
        # check pic exgister
        if self.request.files == {} or 'pic' not in self.request.files:
            self.write('<script>alert("请选择图片")</script>')
            return

        # check pic format
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png']
        send_file = self.request.files['pic'][0]

        if send_file['content_type'] not in image_type_list:
            self.write('<script>alert("仅支持jpg,jpeg,bmp,gif,png格式的图片！")</script>')
            return
        # check pic size 4M
        if len(send_file['body']) > 4 * 1024 * 1024:
            self.write('<script>alert("请上传4M以下的图片");</script>')
            return

        # create temp file
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)

        # illegal pic can't open with Image
        try:
            image_one = Image(tmp_file.name)
        except IOEturerror:
            logging.info(error)
            logging.info('+'*30 + '\n')
            logging.info(self.request.headers)
            tmp_file.close()
            self.write('<script>alert("图片不合法！")</script>')
            return

        # check pixel
        if image_one.columns() < 250 or image_one.rows() < 250 or \
                image_one.columns() > 2000 or image_one.rows() > 2000:
            tmp_file.close()
            self.write('<script>alert("图片长宽在250px~2000px之间！")</script>')
            return

        # saving two type
        image_path = "./static/pic/goods/"
        image_format = send_file['filename'].split('.').pop().lower()
        thumbnail_174 = image_path + str(int(time.time())) + '_1.' + image_format
        image_one.quality(100)
        image_one.scale('174x174')
        image_one.write(str(thumbnail_174))

        thumbnail_94 = image_path + str(int(time.time())) + '_2.' + image_format
        image_one.quality(100)
        image_one.scale('94x94')
        image_one.write(str(thumbnail_94))

        # close temp
        tmp_file.close()
        self.write('<script>alert("文件上传成功")</script>')

        # all arguments, post data
        item_keys = ['catalog', 'name', 'subname', 'price', 'discount']
        item = dict()
        if obj:
            item = self.db.goods.find_one({'_id':Object(obj)})
        for key in item_keys:
            item[key] = self.get_argument(key, None)
            item['size1'] = thumbnail_174
            item['size2'] = thumbnail_94

        if obj:
            self.db.goods.save(item)
        else:
            self.db.goods.insert(item)

        self.redirect('/admin', permanent=True)
        return

class RegHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        args = self.request.arguments
        message = {}
        query = {}

        if "login_name" in args and "password" not in args:
            name = self.get_argument("login_name")
            query["name"] = name
            if self.db.users.find_one(query):
                message['errno'] = 1
                message['msg'] = u"用户名已存在，请重新输入"
            else:
                message['errno'] = 0

            self.write(message)

        elif "login_name" in args and "password" in args:
            name = self.get_argument("login_name")
            passwd = self.get_argument("password")
            phone = self.get_argument("phone")

            customer = { "name": name,
                        "passwd": passwd,
                        "phone": phone}
            if self.db.users.insert(customer):
                message['errno'] = 0
            else:
                message['errno'] = 1
                message['msg'] = u"数据库忙，请稍后再试"

            self.write(message)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

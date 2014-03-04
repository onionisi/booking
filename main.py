# coding=utf-8
import uuid
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from pymongo import MongoClient
from tornado.options import define, options
from datetime import *

import tempfile
import logging
import urllib, ast
from pgmagick import Image
import collections

import launcher

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
                (r"/my_info_password", PasswdHandler),
                (r"/my_account_address", AddrHandler),
                (r"/my_account_address_add_form", Add2Handler),
                (r"/my_order_order", MyOrderHandler),
                (r"/my_order_fav", FavHandler),
                (r"/cart", CartHandler),
                (r"/order", OrderHandler),
                (r"/order_show", Oshow_Handler),
                (r"/order_commit", CommitHandler),
                (r"/c_show", Cshow_Handler),
                (r"/admin", Admin_Handler),
                (r"/edit/(G[0-9A-Z]{12})", Admin_Handler),
                (r"/goods", Goods_Handler),
                ]
        settings = dict(
                title = u"NAME",
                template_path = os.path.join(os.path.dirname(__file__), "templates"),
                static_path = os.path.join(os.path.dirname(__file__), "static"),
                ui_modules = {
                    "Good": GoodModule,
                    "Order": OrderModule,
                    "Index": IndexModule,
                    "Cart": CartModule,
                    "Addr": AddrModule,
                    "Order": OrderModule,
                    "Orgd": OrgdModule,
                    },
                #xsrf_cookies = True,
                cookie_secret = uuid.uuid4(),
                debug = True,
                )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = MongoClient('localhost', 27017).test

class GoodModule(tornado.web.UIModule):
    def render(self, each):
        return self.render_string("modules/good.html", each=each)

class OrderModule(tornado.web.UIModule):
    def render(self, each):
        return self.render_string("modules/order.html", each=each)

class IndexModule(tornado.web.UIModule):
    def render(self, each):
        return self.render_string("modules/index.html", each=each)

class CartModule(tornado.web.UIModule):
    def render(self, each):
        return self.render_string("modules/cart.html", each=each)

class AddrModule(tornado.web.UIModule):
    def render(self, addr, index):
        return self.render_string("modules/addr.html", addr=addr, index=index)

class OrderModule(tornado.web.UIModule):
    def render(self, order):
        return self.render_string("modules/order.html", each=order)

class OrgdModule(tornado.web.UIModule):
    def render(self, order):
        return self.render_string("modules/orgd.html", each=order)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        return self.get_cookie("ln")

class HomeHandler(BaseHandler):
    def get(self):
        entry_all = self.db.goods.find()
        entry_noon = self.db.goods.find({'catalog':'noon'})
        entry_first = self.db.goods.find({'catalog':'first'})
        self.render("index.html", entry_all=entry_all, entry_first=entry_first)

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
    def get(self):
        if self.get_current_user():
            self.render("mine.html")
        else:
            self.redirect('/login')

class PasswdHandler(BaseHandler):
    def get(self):
        name = self.get_current_user()
        if name:
            self.render("my_info_passwd.html", account=name)
        else:
            self.redirect('/login')
    def post(self):
        name = self.get_current_user()
        old_passwd = self.get_argument("password")
        new_passwd = self.get_argument("new_password")

        customer = {"name": name, "passwd": old_passwd}
        message = {}

        if self.db.users.find_one(customer):
            self.db.users.update(customer, {"$set": {"passwd": new_passwd}})
            message['errno'] = 0
        else:
            message['errno'] = 1
            message['msg'] = u"密码输入不正确"

        self.write(message)

class AddrHandler(BaseHandler):
    def get(self):
        if self.request.arguments:
            oid = self.get_argument("order_id")
        else:
            oid = ""
        name = self.get_current_user()
        customer = {"name": name}
        addrs = []
        if name:
            one = self.db.users.find_one(customer)
            if 'addrs' in one:
                addrs = one['addrs']

            self.render("my_account_address.html", addrs=addrs, oid=oid)
        else:
            self.redirect('/login')

class MyOrderHandler(BaseHandler):
    def get(self):
        name = self.get_current_user()
        customer = {"name": name}
        entries = []
        if name:
            # TODO: just everyone last 10 record, del others
            orders = self.db.order.find({'name':name})
            for order in orders:
                entry = {}
                images = []
                money = 0

                goods = order['good']
                count = len(goods)
                for (k,v) in goods.items():
                    each = self.db.goods.find_one({'_id':k})
                    images.append(each['image2'])
                    if each['discount']:
                        money += float(each['discount'])*int(v)
                    else:
                        money += float(each['price'])*int(v)

                entry['oid']=order['_id']
                if 'time' in order:
                    entry['commit']=True
                else:
                    entry['commit']=False

                if count > 2:
                    entry['images']=images[:2]
                else:
                    entry['images']=images

                entry['money']=money
                entry['count']=count

                entries.append(entry)
            self.render("my_order_order.html", orders=iter(entries))
        else:
            self.redirect('/login')

class Add2Handler(BaseHandler):
    def get(self):
        oid = self.get_argument("order_id")
        if self.get_current_user():
            self.render("my_account_address_add_form.html", oid=oid)
        else:
            self.redirect('/login')
    def post(self):
        addr = self.get_argument("address")
        zone = self.get_argument("city_id")
        mobile = self.get_argument("mobile")
        receiver = self.get_argument("receiver")
        new_addr = { 'address':addr,
                'zone':zone,
                'mobile':mobile,
                'receiver':receiver
                }

        name = self.get_current_user()
        customer = {"name": name}
        message = {}
        addr = []

        addrs = self.db.users.find_one(customer, {"addrs": 1})
        if 'addrs' in addrs:
            addrs['addrs'].append(new_addr)
            self.db.users.update(customer, {"$set": {"addrs": addrs['addrs']}})
        else:
            addr.append(new_addr)
            self.db.users.update(customer, {"$set": {"addrs": addr}})

        message['errno'] = 0
        self.write(message)


class FavHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.render("my_order_fav.html")
        else:
            self.redirect('/login')

class OrderHandler(BaseHandler):
    def post(self):
        name = self.get_current_user()
        if not name:
            self.redirect('/login')
        else:
            self.clear_cookie("cartn")
            self.clear_cookie("carts")

            all_args = self.request.arguments

            if 'oder' in all_args:
                tmp = ast.literal_eval(self.get_argument("oder"))
                goods = tmp['gcart']
                oid = 'D'+(str(uuid.uuid4()).split('-'))[4].upper()

                order = {'_id': oid,
                        'name': name,
                        'good': goods}

                self.db.order.insert(order)

            self.redirect('/order_show?order_id=%s' % oid)

class Oshow_Handler(BaseHandler):
    # def Checktime(self, ordertime):
    #     flag=False
    #     starttime=time.strptime(starttime,'%Y-%m-%d %H:%M:%S')
    #     endtime=time.strptime(endtime,'%Y-%m-%d %H:%M:%S')
    #     ordertime=time.strptime(str(ordertime),'%Y-%m-%d %H:%M:%S')

    #     if int(time.mktime(starttime))<= int(time.mktime(weibotime)) and int(time.mktime(endtime))>=int(time.mktime(ordertime)):
    #         flag=True
    #     else:
    #         flag=False

    #     return flag

    def get(self):
        name = self.get_current_user()
        if not name:
            self.redirect('/login')
        else:
            all_args = self.request.arguments
            customer = self.db.users.find_one({"name": name})
            entry=[]
            money=0

            if 'order_id' in all_args:
                oid = self.get_argument("order_id")
                if 'addrs' in customer:
                    addr_id = 0
                    addr = customer['addrs'][addr_id]
                else:
                    addr_id = None
                    addr = None

                order = self.db.order.find_one({'_id':oid})
                goods = order['good']

            for (k,v) in goods.items():
                each = self.db.goods.find_one({'_id':k})
                each['count'] = int(v)
                entry.append(each)
                if each['discount']:
                    money += float(each['discount'])*int(v)
                else:
                    money += float(each['price'])*int(v)
            self.render("order_show.html", entry=entry, money=money*100, oid=oid, addr=addr, addr_id=addr_id)

    def post(self):
        name = self.get_current_user()
        if not name:
            self.redirect('/login')
        else:
            all_args = self.request.arguments
            customer = self.db.users.find_one({"name": name})
            entry=[]
            money=0

            if 'order_id' in all_args:
                oid = self.get_argument("order_id")
                addr_id = self.get_argument("myaddr2")
                addr = customer['addrs'][int(addr_id)]

                order = self.db.order.find_one({'_id':oid})
                goods = order['good']

            for (k,v) in goods.items():
                each = self.db.goods.find_one({'_id':k})
                each['count'] = int(v)
                entry.append(each)
                if each['discount']:
                    money += float(each['discount'])*int(v)
                else:
                    money += float(each['price'])*int(v)
            self.render("order_show.html", entry=entry, money=money*100, oid=oid, addr=addr, addr_id=addr_id)

class CommitHandler(BaseHandler):
    def post(self):
        name = self.get_current_user()
        if not name:
            self.redirect('/login')
        else:
            print ("------------")
            print(self.request.arguments)
            print ("------------")

            # what and cost
            dishes = []
            cost = 0
            oid = self.get_argument("order_id")
            order = self.db.order.find_one({'_id':oid})
            goods = order['good']
            for (k,v) in goods.items():
                each = self.db.goods.find_one({'_id':k})
                dishes.append(each['name'])
                if each['discount']:
                    cost += float(each['discount'])*int(v)
                else:
                    cost += float(each['price'])*int(v)

            # who and where
            addr_id = self.get_argument("myaddr")
            customer = self.db.users.find_one({"name": order['name']})
            addr = customer['addrs'][int(addr_id)]

            # TODO: when, need to fixup with datetime
            send_t = self.get_argument("send_type")
            if send_t == '1':
                now = datetime.now()
                time = now.strftime('%Y-%m-%d %H:%M:%S')
            elif send_t == '2':
                ap_date = self.get_argument("appoint_date")
                ap_time = self.get_argument("appoint_time")
                time = ap_date + ap_time

            # pay
            pay_t = self.get_argument("pay_type")
            if pay_t == '1':
                pay = "face"
            elif pay_t == '2':
                pay = "alipay"

            msg = self.get_argument("message")

            send = {'order':dishes,
                    'cost':cost,
                    'name':addr['receiver'],
                    'phone':addr['mobile'],
                    'addr':addr['address'],
                    'time':time,
                    'pay':pay
                    }

            launch = launcher.Lancher()
            launch.send_data(send)
            save = {'time':time, 'pay':pay }
            order.update(save)
            self.db.order.update({'_id':oid}, order)

            self.render("order_succ.html")

class CartHandler(BaseHandler):
    def get(self):
        if self.request.arguments:
            gid = self.get_argument("goods_id")
            num = int(self.get_argument("num"))
            entry = {}
            entry[gid]=num
            gmcart = {'mcart':[]}

            cartn = self.get_cookie("cartn")
            if cartn:
                tmp = self.get_cookie("carts")
                carts = ast.literal_eval(urllib.unquote(tmp))
                if gid in carts['gcart']:
                    carts['gcart'][gid] = int(carts['gcart'][gid])
                    carts['gcart'][gid] += num
                    if num == 0:
                        self.set_cookie("cartn", str(int(cartn) - 1))
                else:
                    self.set_cookie("cartn", str(int(cartn) + 1))
                    carts['gcart'].update(entry)
                print(carts)
                self.write(carts)
            else:
                self.set_cookie("cartn", str(1))
                gmcart['gcart'] = entry
                print(gmcart)
                self.write(gmcart)
        else:
            entry = []
            tmp = self.get_cookie("carts")
            if tmp:
                carts = ast.literal_eval(urllib.unquote(tmp))
                for (k,v) in carts['gcart'].items():
                    each = self.db.goods.find_one({'_id':k})
                    entry.append(each)
            self.render("cart.html", entry=entry)

class Goods_Handler(BaseHandler):
    def get(self):
        gid = self.get_argument("goods_id")
        entry = self.db.goods.find_one({'_id':gid})
        user = self.get_current_user()
        if user == "admin":
            permit = True
        else:
            permit = False
        self.render("good.html", entry=entry, permit=permit)

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
        message = {}

        if self.db.users.find_one(customer):
            # TODO: need to use uid instead name
            self.set_cookie("ln", name)
            message['errno'] = 0
            message['msg'] = u"欢迎光临"
        else:
            message['errno'] = 1
            message['msg'] = u"帐号或者密码不正确"

        self.write(message)

class Admin_Handler(BaseHandler):
    def get(self, gid=None):
        good = dict()
        if gid:
            good = self.db.goods.find_one({'_id':gid})

        if self.get_current_user() == 'admin':
            self.render("edit.html", entry=good)
        else:
            self.redirect('/login')

    def post(self, gid=None):
        good_keys = ['catalog', 'name', 'subname', 'price', 'discount']
        good = dict()
        if gid:
            good = self.db.goods.find_one({'_id':gid})
        for key in good_keys:
            good[key] = self.get_argument(key, None)

        if gid:
            self.db.goods.save(good)
        else:
            #========= new id generate
            gid = 'G'+(str(uuid.uuid4()).split('-'))[4].upper()

            #========= image handler
            # check pic exgister
            if self.request.files == {} or 'pic' not in self.request.files:
                self.write('<script>alert("请选择图片")</script>')

            send_file = self.request.files['pic'][0]
            # check pic format
            image_type = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png']
            if send_file['content_type'] not in image_type:
                self.write('<script>alert("仅支持jpg,jpeg,bmp,gif,png格式的图片")</script>')

            # check pic size 4M
            if len(send_file['body']) > 4 * 1024 * 1024:
                self.write('<script>alert("请上传4M以下的图片");</script>')

            # create temp file
            tmp_file = tempfile.NamedTemporaryFile(delete=True)
            tmp_file.write(send_file['body'])
            tmp_file.seek(0)

            # illegal pic can't open with Image
            try:
                image_one = Image(tmp_file.name)
            except IOError:
                logging.info(error)
                logging.info('+'*30 + '\n')
                logging.info(self.request.headers)
                tmp_file.close()
                self.write('<script>alert("图片不合法！")</script>')

            # check pixel
            if image_one.columns() < 250 or image_one.rows() < 250 or \
                    image_one.columns() > 2000 or image_one.rows() > 2000:
                tmp_file.close()
                self.write('<script>alert("图片长宽在250px~2000px之间！")</script>')

            # saving two type
            image_path = "./static/images/goods/"
            image_format = send_file['filename'].split('.').pop().lower()
            thumbnail_174 = image_path + gid + '_174.' + image_format
            image_one.quality(100)
            image_one.scale('174x174')
            image_one.write(str(thumbnail_174))

            thumbnail_94 = image_path + gid + '_94.' + image_format
            image_one.quality(100)
            image_one.scale('94x94')
            image_one.write(str(thumbnail_94))

            # close temp
            tmp_file.close()

            good['_id'] = gid
            good['image1'] = thumbnail_174
            good['image2'] = thumbnail_94

            self.db.goods.insert(good)

        self.redirect('/admin', permanent=True)

class RegHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        args = self.request.arguments
        message = {}
        query = {}
        # li = self.db.invites.find_one()

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
            # phone = self.get_argument("phone")

            # invite = self.get_argument("invite")
            # if invite in li['invite']:
            #     li = [i for i in li if i!=invite]
            # else:
            #     self.redirect('/')

            uid = 'G'+(str(uuid.uuid4()).split('-'))[4].upper()
            now = datetime.now()
            reg_tm = now.strftime('%Y-%m-%d %H:%M:%S')
            customer = {"_id": uid,
                        "name": name,
                        "passwd": passwd,
                        "date": reg_tm}
            if self.db.users.insert(customer):
                self.set_cookie("ln", name)
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

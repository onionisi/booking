# coding=utf8

import tornado.web
import tempfile
import time
import logging
from pgmagick import Image

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        # check pic exgister
        if self.request.files == {} or 'pic' not in self.request.files:
            self.write('<script>m_ksb_msg.show("请选择图片")</script>')
            return

        # check pic format
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png']
        send_file = self.request.files['pic'][0]

        if send_file['content_type'] not in image_type_list:
            self.write('<script>m_ksb_msg.show("仅支持jpg,jpeg,bmp,gif,png格式的图片！")</script>')
            return
        # check pic size 4M
        if len(send_file['body']) > 4 * 1024 * 1024:
            self.write('<script>m_ksb_msg.show("请上传4M以下的图片");</script>')
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
            self.write('<script>m_ksb_msg.show("图片不合法！")</script>')
            return

        # check pixel
        if image_one.columns() < 250 or image_one.rows() < 250 or \
                image_one.columns() > 2000 or image_one.rows() > 2000:
            tmp_file.close()
            self.write('<script>m_ksb_msg.show("图片长宽在250px~2000px之间！")</script>')
            return

        # saving
        image_path = "./static/pic/goods/"
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = image_path + str(int(time.time())) + image_format
        image_one.write(tmp_name)

        # close temp
        tmp_file.close()
        self.write('<script>m_ksb_msg.show("文件上传成功，路径为：" + image_path[1:])</script>')
        return

    # if self.request.files:
    #     for f in self.request.fiels['postfile']:
    #         rawname = f['filename']
    #         dstname = str(int(time.time())) + '.' + rawname.split('.').pop()
    #         thbname = "thumb_" + dstname
    #         # write a file
    #         # src = "./static/upload/src/" + dstname
    #         # file(src, 'w+').write(f['body'])
    #         tf = tempfile.NamedTemporaryFile()
    #         tf.write(f['body'])
    #         tf.seek(0)

    #         # create normal file
    #         # img = Image.open(src)
    #         img = Image.open(tf.name)
    #         img.thumnail((920, 920), resample=1)
    #         img.save("./static/upload/postfiles/"+dstname)

    #         # create thunm file
    #         img.thumbnail((100, 100), resample=1)
    #         img.save("./static/upload/postfiles/"+thbname)

    #         tf.close()

from tornado.httpclient import AsyncHTTPClient

def handle_request(response):
    if response.error:
        print "Error:", respone.error
    else:
        print response.body

http_client = AsyncHTTPClient()
http_client.fetch("http://localhost:8888", handle_request)

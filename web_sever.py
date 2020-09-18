"""
web sever

完成一个类,提供给别人
让他可以用这个类快速的搭建后端web服务
"""
from socket import *
from select import select
import re


# 功能类
class WebSever:
    def __init__(self, host="0.0.0.0", port=8000, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    def handle(self, connfd):
        # 浏览器发过来请求
        request = connfd.recv(1024).decode()
        # 解析请求(请求内容)
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)
        if result:
            info = result.group("info")
            print(info)
            self.send_response(connfd, info)
        else:
            # 没有匹配到内容
            self.rlist.remove(connfd)
            connfd.close()
            return

    def send_response(self, connfd, info):
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        #     打开失败文件不存在
        try:
            file = open(filename, "rb")
            
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry.....</h1>"
            response = response.encode()
        else:
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % (len(data))
            response += "\r\n"
            response = response.encode() + data

        finally:
            # 发送响应给客户端
            connfd.send(response)

    # 启动服务
    def start(self):
        # 设置监听
        self.sock.listen(5)
        print("Listen  the port %d " % self.port)
        # 首先加入监听套接字
        self.rlist.append(self.sock)
        while True:
            # 监控关注的IO
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            # 遍历就绪的IO列表，分情况讨论　监听套接字和客户端
            for i in rs:
                if i is self.sock:
                    # 浏览器连接
                    connfd, addr = self.sock.accept()
                    # 将连接进来的客户端链接套接字加入关注的IO
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    try:
                        self.handle(i)
                    except:
                        self.rlist.remove(i)
                        i.close()


if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = 8000
    httpd = WebSever(host=HOST, port=PORT, html="./static")
    httpd.start()

"""
练习 : 将 first.html作为一个要展示的网页
当用户的请求内容是 /first.html的时候则将这个
网页内容作为一个响应体提供给浏览器

如果浏览器请求的是其他内容则 返回一个404的响应,
内容自定

要求浏览器可以循环的访问

思路 : 1 服务端循环模型
      2. 接收到请求后要提取请求内容
      3. 根据请求内容分情况讨论
"""
from socket import *

HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST,PORT)

# 创建tcp网络
sockfd = socket()
sockfd.bind(ADDR)
sockfd.listen(5)

while True:
    connfd,addr = sockfd.accept()
    # 接收http请求
    request = connfd.recv(1024).decode()
    # 防止返回值为空
    if not request:
        continue

    # 提取出请求内容
    info = request.split(' ')[1]
    print("请求内容:",info)

    if info == '/first.html':
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        with open('first.html') as f:
            response += f.read()
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Sorry.....</h1>"

    # 发送响应
    connfd.send(response.encode())



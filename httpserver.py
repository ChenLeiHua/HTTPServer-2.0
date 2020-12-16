from socket import *
from select import *


class HTTPServer:
    def __init__(self, addr=('0.0.0.0', 8000), _dir='./static'):
        self.host = addr[0]
        self.port = addr[1]
        self.dir = _dir
        self.addr = addr
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.sockfd.bind(self.addr)

    def handle(self, c):
        request = c.recv(4096)
        if not request:
            self.rlist.remove(c)
            c.close()
            return
        # 解析请求参数
        # 字节串按行分割
        request_line = request.splitlines()[0].decode()
        request_url = request_line.split(' ')[1]
        print(request_url)
        request_method = request_line[0]
        if request_url == '/' or request_url[-5:] == '.html':
            self.get_html(c, request_url)
        else:
            self.get_data()
        # print(c.getpeername(), ':', request_url)

    def get_html(self, c, data):
        if data == '/':
            file = self.dir + '/index.html'

        else:
            file = self.dir + data

        try:
            fd = open(file, encoding='utf8')
        except Exception as e:
            response = 'HTTP/1.1 404 Not Found\r\n'
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += '<h1>Sorry......</h1>'
        else:
            response = 'HTTP/1.1 200\r\n'
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += fd.read()
        finally:
            c.send(response.encode())

    def get_data(self):
        pass

    # 启动服务
    def server_forever(self):
        self.sockfd.listen(5)
        print('正在监听 %d 端口......' % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs, = select(self.rlist,
                                 self.wlist,
                                 self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = self.sockfd.accept()
                    print('客户端 %s 已连接' % addr[0])
                    self.rlist.append(c)

                if r is c:
                    self.handle(r)


if __name__ == '__main__':
    """
    用户使用时，通过导入类即可快速搭建服务，展示网页
    """
    ADDR = ('0.0.0.0', 8000)
    DIR = '/static'
    http = HTTPServer(ADDR)
    http.server_forever()  # 启动服务

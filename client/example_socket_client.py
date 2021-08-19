import socket
from threading import Thread


CLINET_MAX=5
BUFFER_SIZE=2**12

class SocketClient(object):
    def __init__(self,host = '127.0.0.1', port = 14567):
        # 明确配置变量
        ip_port = (host,port)
        # 创建一个TCP套接字
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
        self.ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
        # 绑定端口号
        self.ser.connect(ip_port)  # 写哪个ip就要运行在哪台机器上
        rec = self.ser.recv(BUFFER_SIZE)
        print(rec.decode())
    def start_context(self,data):
        self.ser.send(data.encode())
        return self.ser.recv(BUFFER_SIZE)
    def __enter__(self,host = '127.0.0.1', port = 14567):
        obj = self.__init__(host,port)
        return obj
    def __exit__(self, exc_type, exc_val, exc_tb):

        self.ser.close()


if __name__ == '__main__':
    cli = SocketClient()
    while True:
        print("请输入input")
        data = input()
        rec = cli.start_context(data)
        print(rec.decode())
    cli.ser.close()

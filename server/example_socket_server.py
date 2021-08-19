import socket
from threading import Thread


CLINET_MAX=5
BUFFER_SIZE=2**12

class SocketServer(object):
    def __init__(self,host = '127.0.0.1', port = 14567):
        # 明确配置变量
        ip_port = (host,port)
        # 创建一个TCP套接字
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字类型AF_INET, socket.SOCK_STREAM   tcp协议，基于流式的协议
        self.ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
        # 绑定端口号
        self.ser.bind(ip_port)  # 写哪个ip就要运行在哪台机器上
        # 设置半连接池
        self.ser.listen(CLINET_MAX)  # 最多可以连接多少个客户端
        self.user_list = []
        print("服务器启动成功，正在等待用户连接")
        while 1:
            # 阻塞等待，创建连接
            con, address = self.ser.accept()  # 在这个位置进行等待，监听端口号
            print(f"{address}连接了")
            self.user_list.append(address)
            print(f"用户当前ID为{len(self.user_list)}")
            t = Thread(target=self.handel_context,args=(con,address,len(self.user_list)))
            t.setDaemon(True)
            t.start()
    def handel_context(self,con,address,user_index):
        con.sendall(f"连接服务器成功,用户ID：{user_index}".encode())
        while 1:
            try:
                # 接受套接字的大小，怎么发就怎么收
                msg = con.recv(BUFFER_SIZE)
                if msg.decode('utf-8') == '1':
                    # 断开连接
                    con.close()
                elif msg.decode()=="2":
                    to_send=f"当前在线用户数量{len(self.user_list)}"
                else:
                    to_send = "你输入的是"+msg.decode()
                print('服务器收到消息', msg.decode('utf-8'),f"\t消息来自用户{user_index}")
                con.sendall(to_send.encode())
            except Exception as e:
                break
        print(f"连接已断开，{address}")
        # 多线程需要优化 用户列表pop操作
        self.user_list.pop(user_index-1)
    def __enter__(self,host = '127.0.0.1', port = 14567):
        obj = self.__init__(host,port)
        return obj
    def __exit__(self, exc_type, exc_val, exc_tb):

        self.ser.close()


if __name__ == '__main__':
    ser = SocketServer()
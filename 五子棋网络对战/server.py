import socket
import threading
from chessboard import *
from chessman import *
from engine import *
from usergothread import *
from computergothread import *


class ServerThread1(threading.Thread):
    def __init__(self,engine,chessmanClient,clientSocket):
        super().__init__()
        self.engine=engine
        self.chessmanClient=chessmanClient
        self.clientSocket=clientSocket

    def run(self):
        while True:
            recv=self.clientSocket.recv(1024)
            recvClientInput=str(recv.decode('gbk'))
            print('用户下棋位置:%s'%recvClientInput)
            self.engine.parseUserInputStr(recvClientInput,self.chessmanClient)
            self.chessmanClient.doNotify()
            self.chessmanClient.doWait()


class ServerThread2(threading.Thread):
    def __init__(self,engine,chessmanServer,clientSocket):
        super().__init__()
        self.engine=engine
        self.chessmanServer=chessmanServer
        self.clientSocket=clientSocket

    def run(self):
        while True:
            self.chessmanServer.doWait()
            serverInput = input('请输入下棋坐标:')
            self.engine.parseUserInputStr(serverInput, self.chessmanServer)
            self.clientSocket.send(serverInput.encode('gbk'))
            self.chessmanServer.doNotify()


def main():
    #创建棋盘并初始化
    chessboard=ChessBoard()
    chessboard.initBoard()
    #chessboard.printBoard()
    #引擎对象
    engine=Engine(chessboard)

    chessmanClient = ChessMan()
    chessmanClient.setColor('x')  # 用户黑棋
    chessmanServer = ChessMan()
    chessmanServer.setColor('o')  # 服务端白棋

    serverSocket=None
    try:
        print('启动服务器')

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverPort = 8080
        print('绑定端口号为:%d' % serverPort)
        # 一般服务端的ip地址设置为空即可，默认查找最合适的ip地址
        serverInfo = ('', serverPort)
        # 绑定服务端
        serverSocket.bind(serverInfo)

        # listen监听
        serverSocket.listen(5)

        #clientScoket=None

        print('开始接收客户端的连接')
        while True:
            # accept接收客户端连接
            # 第一个返回值描述连接的客户端socket对象
            # 第二个返回值是长度为2的元组，描述连接客户端的ip地址和端口号
            clientSocket, clientInfo = serverSocket.accept()
            print('接收到客户端连接,ip地址为:%s,端口号为:%s'%(clientInfo[0],clientInfo[1]))
            t1 = ServerThread1(engine, chessmanClient, clientSocket)
            t2 = ServerThread2(engine, chessmanServer, clientSocket)
            t1.start()
            t2.start()

            while clientInfo!=None:
                print('等待对方下棋.....')
                chessmanClient.doWait()
                chessboard.setChessMan(chessmanClient)
                chessboard.printBoard()
                pos = chessmanClient.getPos()
                if engine.isWon(pos, 'x'):
                    print('哈哈，你输了')
                    break
                chessmanServer.doNotify()
                chessmanServer.doWait()
                chessboard.setChessMan(chessmanServer)
                chessboard.printBoard()
                pos = chessmanServer.getPos()
                if engine.isWon(pos, 'o'):
                    print('恭喜，你终于赢了')
                    break
                chessmanClient.doNotify()

    except:
        pass
    finally:
        #关闭socket
        print('关闭服务端')
        serverSocket.close()

if __name__=='__main__':
    main()



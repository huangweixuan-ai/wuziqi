import socket
import threading
from chessboard import *
from chessman import *
from engine import *
from usergothread import *
from computergothread import *

class ClientThread1(threading.Thread):
    def __init__(self,engine,chessmanClient,clientSocket):
        super().__init__()
        self.engine=engine
        self.chessmanClient=chessmanClient
        self.clientSocket=clientSocket

    def run(self):
        while True:
            userInput = input('请输入下棋坐标:')
            self.engine.parseUserInputStr(userInput, self.chessmanClient)
            self.clientSocket.send(userInput.encode('gbk'))
            self.chessmanClient.doNotify()
            self.chessmanClient.doWait()


class ClientThread2(threading.Thread):
    def __init__(self,engine,chessmanServer,clientSocket):
        super().__init__()
        self.engine=engine
        self.chessmanServer=chessmanServer
        self.clientSocket=clientSocket

    def run(self):
        while True:
            self.chessmanServer.doWait()
            recv = self.clientSocket.recv(1024)
            recvServerInput=str(recv.decode('gbk'))
            print('对方下棋位置:%s' % recvServerInput)
            self.engine.parseUserInputStr(recvServerInput,self.chessmanServer)
            self.chessmanServer.doNotify()


def main():
    #创建棋盘并初始化
    chessboard=ChessBoard()
    chessboard.initBoard()
    chessboard.printBoard()
    #引擎对象
    engine=Engine(chessboard)

    chessmanClient=ChessMan()
    chessmanClient.setColor('x')#用户黑棋
    chessmanServer = ChessMan()
    chessmanServer.setColor('o')#服务端白棋

    clientSocket = None
    try:
        print('启动客户端')
        # 创建流式套接字(TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 服务器地址
        serverAddress = '192.168.56.9'
        serverPort = 8080
        print('连接服务器的地址为:%s,端口号为:%d'%(serverAddress,serverPort))
        serverInfo = (serverAddress, serverPort)
        clientSocket.connect(serverInfo)

        t1=ClientThread1(engine,chessmanClient,clientSocket)
        t2=ClientThread2(engine,chessmanServer,clientSocket)
        t1.start()
        t2.start()

        while True:
            chessmanClient.doWait()
            chessboard.setChessMan(chessmanClient)
            chessboard.printBoard()
            pos = chessmanClient.getPos()
            if engine.isWon(pos, 'x'):
                print('恭喜，你终于赢了')
                break
            print('等待对方下棋.....')
            chessmanServer.doNotify()
            chessmanServer.doWait()
            chessboard.setChessMan(chessmanServer)
            chessboard.printBoard()
            pos = chessmanServer.getPos()
            if engine.isWon(pos, 'o'):
                print('哈哈，你输了')
                break
            chessmanClient.doNotify()

    except Exception as e:
        print(e)
    finally:
        #关闭socket
        print('关闭客户端')
        clientSocket.close()

if __name__=='__main__':
    main()


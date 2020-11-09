import threading


class UserGoThread(threading.Thread):
    '''用户下棋线程'''
    def __init__(self,engine,chessmanUser):
        super().__init__()
        self.engine=engine
        self.chessmanUser=chessmanUser

    def run(self):
        while True:
            #1.用户从终端输入下棋坐标
            userInput=input('请输入下棋坐标:')
            self.engine.parseUserInputStr(userInput,self.chessmanUser)
            #2.用户notify
            self.chessmanUser.doNotify()
            #3.用户wait
            self.chessmanUser.doWait()

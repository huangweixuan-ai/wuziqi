
import random
from chessman import *
from chessboard import *

class Engine(object):
    '''引擎类，实现下棋的策略的规则'''
    def __init__(self,chessboard): #chessboard是棋盘的对象
        if not  isinstance(chessboard,ChessBoard):
            raise Exception('参数必须为Chessboard对象')
        self.__chessboard=chessboard

    def computerGo(self,chessman):
        '''电脑下棋的策略'''
        if not isinstance(chessman,ChessMan):
            raise Exception('参数必须为ChessMan对象')
        while True: #循环生成随机数
            posX=random.randint(1,15)
            posY=random.randint(1,15)
            if self.__chessboard.getChess((posX,posY))=='+': #判断随机坐标是否为空，空则写入ChessMan对象中
                print('电脑下棋的位置：%d,%d' % (posX, posY))
                chessman.setPos((posX, posY)) #把posX和posY放进ChessMan对象中
                break
    def parseUserInputStr(self,inputStr,chessman):
        '''
        用户在终端下棋
        提示用户 传入用户输入的字符串 解析该字符串对应的位置
        传入chessman对象的时候 把棋子的颜色写入
        在该方法仲负责填写棋子的位置
        '''
        if not isinstance(chessman,ChessMan):
            raise Exception('第2个参数必须为ChessMan对象')
        ret=inputStr.split(',')
        value1=ret[0]
        value2=ret[1]
        #转换成坐标
        posX=int(value1)
        posY=ord(value2)-ord('a')+1
        chessman.setPos((posX,posY))

    def isWon(self,pos,color):
        '''
        判断是否影棋
        当在pos位置上放置的color颜色的棋子后，是否胜负已分
        返回True表示胜负已分
        '''
        if not isinstance(pos,tuple):
            raise Exception('第一个参数必须为元组')
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        '''垂直方向'''
        startX=1
        if pos[0]-4>=1:
            startX=pos[0]-4
        endX=ChessBoard.BOARD_SIZE
        if pos[0]+4<=ChessBoard.BOARD_SIZE:
            endX=pos[0]+4
        count=0
        for posX in range(startX,endX+1):
            if self.__chessboard.getChess((posX,pos[1]))==color:
                count+=1
                if count>=5:
                    return True
            else:
                count=0
        '''水平方向'''
        startY = 1
        if pos[1] - 4 >= 1:
            startY = pos[1] - 4
        endY = ChessBoard.BOARD_SIZE
        if pos[1] + 4 <= ChessBoard.BOARD_SIZE:
            endY = pos[1] + 4
        count = 0
        for posY in range(startY, endY + 1):
            if self.__chessboard.getChess((pos[0], posY)) == color:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 0
        '''左上右下方向'''
        count = 0
        for posX in range(startX, endX + 1):
            for posY in range(startY,endY+1):
                if self.__chessboard.getChess((posX, posY)) == color:
                    count += 1
                    posY+=1
                    posX+=1
                    if posX > 15:
                        posX = 15

                    if count >= 5:
                        return True
                else:
                    count = 0


        '''右上左下方向'''
        count2 = 0
        for posX in range(startX, endX + 1):
            for posY in range(endY,startY-1,-1):
                if self.__chessboard.getChess((posX, posY)) == color:
                    count2 += 1
                    posY -= 1
                    posX += 1
                    if posX > 15:
                        posX = 15
                    if count2 >= 5:
                        return True
                else:
                    count2 = 0

        return False

    def play(self):
        '''主流程'''
        userBlack=True
        userDown=True
        while True:
            #外循环开始
            #1.用户选择先后
            userInput=input('请选择黑棋或白棋，b为黑棋,w为白棋')
            if userInput.startswith('w'):
                userBlack=False
                userDown=False
            #2.初始化棋盘
            self.__chessboard.initBoard()
            self.__chessboard.printBoard()
            while True:
                #内循环开始
                chessmanUser=ChessMan()
                chessmanPC=ChessMan()
                if userBlack:
                    chessmanUser.setColor('x')
                    chessmanPC.setColor('o')
                else:
                    chessmanUser.setColor('o')
                    chessmanPC.setColor('x')
                #3.是否轮到用户下
                #if xxx:
                    #4-1.如果轮到用户下
                #else:
                    #4-2.如果轮到电脑下
                if userDown:
                    print('轮到用户下')
                    userInput=input('请输入下棋坐标:')
                    self.parseUserInputStr(userInput,chessmanUser)
                    self.__chessboard.setChessMan(chessmanUser)
                else:
                    print('轮到电脑下')
                    self.computerGo(chessmanPC)
                    self.__chessboard.setChessMan(chessmanPC)
                self.__chessboard.printBoard()
                #5.判断是否赢棋
                    #如果赢棋，则退出内循环
                    #如果没有赢棋，则切换下棋方
                if userDown:
                    pos=chessmanUser.getPos()
                    color=chessmanUser.getColor()
                    if self.isWon(pos,color):
                        print('恭喜，你终于赢了')
                        break
                    else:
                        userDown=not userDown
                else:
                    pos = chessmanPC.getPos()
                    color = chessmanPC.getColor()
                    if self.isWon(pos, color):
                        print('哈哈，你输了')
                        break
                    else:
                        userDown = not userDown
            #内循环结束，外循环继续
            #7.判断是否继续游戏
                #如果用户选择继续游戏，则外循环继续
                #如果用户选择退出，则退出外循环
            userInput=input('是否继续？(y/n)')
            if userInput.startswith('n'):
                break





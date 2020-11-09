
from chessman import *

class ChessBoard(object):
    BOARD_SIZE=15 #棋盘大小
    def __init__(self):
        '''初始化、棋盘索引'''
        self.__board=[] #二维坐标
        for i in range(0,ChessBoard.BOARD_SIZE+1):
            line=[] #一维坐标 表示棋盘上的一行
            for j in range(0,ChessBoard.BOARD_SIZE+1):
                line.append(0) #一个坐标点
            self.__board.append(line)

    def initBoard(self):
        '''清空棋盘'''
        #忽略第0行
        for i in range(1,ChessBoard.BOARD_SIZE+1):
            for j in range(1,ChessBoard.BOARD_SIZE+1):
                self.__board[i][j]='+'

    def printBoard(self):
        '''打印棋盘'''
        print('  ',end='')#列号对齐
        for i in range(1, ChessBoard.BOARD_SIZE + 1): #打印列号
            c=chr(ord('a')+i-1)
            print(c,end='')
        print()
        for i in range(1,ChessBoard.BOARD_SIZE+1):
            print('%2d'%i,end='') #打印行号
            for j in range(1,ChessBoard.BOARD_SIZE+1):
                print(self.__board[i][j],end='')
            print() #换行

    def setChess(self,pos,color): # pos 坐标，必须为列表或元组，长度为2; color 棋子颜色，'x'或'o'
        '''在指定位置放置指定颜色的棋子'''
        if not isinstance(pos,tuple):
            raise Exception('第1个参数必须为元组')
        if pos[0]<=0 or pos[0]>ChessBoard.BOARD_SIZE:
            raise  Exception('下标越界')
        if pos[1]<=0 or pos[1]>ChessBoard.BOARD_SIZE:
            raise  Exception('下标越界')
        self.__board[pos[0]][pos[1]]=color
    def setChessMan(self,chessman): #chessman 棋子ChessMan对象
        '''把chessman对象放置在棋盘上'''
        if not isinstance(chessman,ChessMan):
            raise Exception('第1个参数必须为ChessMan对象')
        pos=chessman.getPos()
        color=chessman.getColor()
        self.setChess(pos,color)
    def getChess(self,pos):
        '''通过坐标读取棋子'''
        if not isinstance(pos,tuple):
            raise Exception('第1个参数必须为元组')
        if pos[0]<=0 or pos[0]>ChessBoard.BOARD_SIZE:
            raise  Exception('下标越界')
        if pos[1]<=0 or pos[1]>ChessBoard.BOARD_SIZE:
            raise  Exception('下标越界')
        return self.__board[pos[0]][pos[1]]
    def isEmpty(self,pos):
        '''判断坐标是否为空'''
        if not isinstance(pos,tuple):
            raise Exception('第一个参数必须为元组')
        if pos[0] <= 0 or pos[0] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if pos[1] <= 0 or pos[1] > ChessBoard.BOARD_SIZE:
            raise Exception('下标越界')
        if self.__board[pos[0]][pos[1]]=='x':
            return False
        elif self.__board[pos[0]][pos[1]]=='o':
            return False
        return True


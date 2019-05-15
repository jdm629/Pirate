#!/usr/bin/env python
PosCenter = ((1036, 368),   (1036, 499),    (1036, 630),    (1036, 761),
            (826, 541),     (875, 449),     (904, 354),     (902, 251),     (824, 195),
            (728, 156),     (639, 195),     (536, 178),     (435, 178),     (404, 273),
            (444, 361),     (510, 445),     (532, 541),     (466, 617),     (357, 647),
            (266, 651),     (179, 626),     (118, 538),      (159, 447),     (217, 364),     (257, 273), 
            (270, 150),     (185, 70),      (74, 84),       (140, 190),     (67, 283))
#各个节点的中心坐标
PosRect = [ [0 for i in range(2)] for i in range(len(PosCenter))]
for i in range(len(PosCenter)):
    PosRect[i][0]=PosCenter[i][0]-43; PosRect[i][1]=PosCenter[i][1]-43
#各个节点的左上角坐标
myRGB = ((255,0,0), (0,255,0), (255,0,255), (255,255,0), (255,255,255), (0,0,0))
Bonus = [0, 0, 0, 0]
#####################################################################
class Qi:                       #棋子
    def __init__(self, cid):
        self.cid = cid          #id0~3为红棋，id4~7为绿棋        

class Node:                     #路径上的节点
    def __init__(self, where): 
        self.where = where  
        self.stack = []
        self.__top = -1          
    def push(self, chess):
        self.stack.append(chess)        
        self.__top += 1 
        #print('push: ',chess.cid)
    def pop(self):
        self.stack.pop()
        self.__top -= 1
        #print('pop_ok')
    def gettopidx(self):
        return self.__top
    def gettopcid(self):        
        return self.stack[self.__top].cid
    def changeWhere(self, w):
        self.where = w    
    def showStack(self):
        print(self.where, self.__top + 1, end = ': ')        
        for i in range(len(self.stack)):         
            print(self.stack[i].cid, end = ' ')

#####################################################################        
def showPathStack():
    for i in range(len(path)):     
        print(''); print('<', i, '>', end = ' ')
        path[i].showStack()

def hasPathStackTop(turn):                  #判断是否本轮棋子全被压住
    for i in range(len(path) - 5):
        if path[i].gettopidx() != -1:
            if int(path[i].gettopcid() / 4) == turn:
                return 'Found'
    return 'notFound'

def whichPos(mx, my):
    #通过鼠标左键时坐标确定节点号
    idx = 0
    mini = 10000
    for i in range(len(PosCenter)): 
        v = math.fabs(mx - PosCenter[i][0]) + math.fabs(my - PosCenter[i][1])
        if v < mini:
            mini = v
            idx = i
    if math.fabs(mx - PosCenter[idx][0]) + math.fabs(my - PosCenter[idx][1]) < 100: #精确选中
        return idx
    else:
        return 'otherPlace'

def moveChess():
    if pos > 3:                                 #上路了
        pos1 = pos + steps
    else:                                       #在家呢
        pos1 = 3 + steps
    if pos1 > 29:                               #冲过头折返
        n = pos1 - 29;  pos1 = 29 - n
    print("Dst:", pos1)

    if path[pos1].where == 'land' or path[pos1].where == 'wood':
        inf = 'onWay'

    if path[pos1].where == 'sea':               #掉进海里
        path[pos1].changeWhere('wood')
        pos1 = int(qiid / 4)                    #回老家
        print("-----GoHome seat:", pos1, end = '  ')
        inf = 'inWater'

    if path[pos1].where == 'someone':           #宝箱已被占
        pos1 = pos        
        print("-----Reserved:", pos1) 
        inf = 'reserved'      

    if path[pos1].where == 'mine':              #进入宝藏区
        path[pos1].changeWhere('someone')       #抢占宝箱
        inf = 'openBox'

    path[pos].pop()
    path[pos1].push(Qi(qiid))
    print("Move OK")
    return infoCase
    #showPathStack() 

def whoWin():
    playerBonus = [0,0,0]
    gameOver = 0
    for i in range(25, 30):
        if path[i].where == 'someone':
            gameOver += 1
            n = int(path[i].gettopcid() / 4)
            playerBonus[n] += (i - 24)
    if gameOver == 51:
        maxv = -1
        for i in range(3):
            if playerBonus[i] > maxv:
                maxv = playerBonus[i]
                maxi = i
        if maxi == 0: infoCase = '0win'
        if maxi == 1: infoCase = '1win'
        if maxi == 2: infoCase = '2win'            


#####################################################################
path = [Node('home'), Node('home'), Node('home'), Node('home'),
        Node('land'), Node('land'), Node('land'), Node('land'), Node('land'), 
        Node('sea'), Node('sea'), Node('land'), Node('land'), Node('land'), 
        Node('land'), Node('sea'), Node('sea'), Node('sea'), Node('land'), 
        Node('land'), Node('land'), Node('sea'), Node('sea'), Node('sea'), Node('sea'),
        Node('mine'), Node('mine'), Node('mine'), Node('mine'), Node('mine')]
#路径初始化
path[0].push(Qi(0));    path[0].push(Qi(1));    path[0].push(Qi(2));    path[0].push(Qi(3))
path[1].push(Qi(4));    path[1].push(Qi(5));    path[1].push(Qi(6));    path[1].push(Qi(7))
path[2].push(Qi(8));    path[2].push(Qi(9));    path[2].push(Qi(10));   path[2].push(Qi(11))
#path[3].push(Qi(12));   path[3].push(Qi(13));   path[3].push(Qi(14));   path[3].push(Qi(15))
#棋子初始化
#showPathStack()
playersNum = 3          #比赛人数

#####################################################################
import pygame                   #导入pygame库
from pygame.locals import *     #导入一些常用的函数和常量
from sys import exit            #向sys模块借一个exit函数用来退出程序
import math 
import random

pygame.init()                   #初始化pygame,为使用硬件做准备
FPS = 100 
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode((1140, 740), FULLSCREEN, 32)    #创建了一个窗口0,NOFRAME,FULLSCREEN
pygame.display.set_caption("小海盗")                    #设置窗口标题
 
background_image = pygame.image.load('board.jpg').convert()
pad_image = pygame.image.load('pad.png').convert_alpha()
chess_image = [ pygame.image.load('player1.png').convert_alpha(), 
                pygame.image.load('player2.png').convert_alpha(),                    
                pygame.image.load('player3.png').convert_alpha()]
#加载并转换图像 

info = {'start': '先按空格键或鼠标右键确定前进的步数，再用鼠标左键点选要走的棋',
        'step6': '当步数为6时，先用鼠标点选要走的棋子，再点选前方1~6步的任意位置',
        'inWater': '棋子落水，返回老家；添加木板，以后不会再落水',
        'reserved': '宝箱已被占用，本轮无效，换下一选手继续',
        'openBox': '抢到一个宝箱！',
        '0win': '红方获胜！',    '1win': '绿方获胜！',    '2win': '紫方获胜！'}

#font = pygame.font.Font("simhei.ttf", 100)
#font = pygame.font.Font("c:\\windows\\fonts\\msyh.ttf", 100)
font = pygame.font.Font("/usr/share/fonts/custom/msyh.ttf", 100)
text_surface = font.render("0", True, myRGB[4])

#infofont = pygame.font.Font("simhei.ttf", 16)
#infofont = pygame.font.Font("c:\\windows\\fonts\\simhei.ttf", 16)
infofont = pygame.font.Font("/usr/share/fonts/custom/simhei.ttf", 16)
info_surface = infofont.render(info['start'], True, myRGB[4])


speed = 200; clock = pygame.time.Clock()
x = 650; y = 610
x1, y1 = PosRect[0] 
dx = 0; dy = 0

qiid = 0                #准备走的棋子
steps = 0               #骰子步数
pos = 'otherPlace'      #节点号


startpos = 3
myTurn = -1             #轮次
canTurn = True
canPick = False
firstPick = True
infoCase = 'start'

while True:
#游戏主循环 
    for event in pygame.event.get():
        if event.type == QUIT:                  #接收到退出事件后退出程序
            exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            exit()

        if (event.type == KEYDOWN and event.key == K_SPACE) or \
            (event.type == MOUSEBUTTONDOWN and event.button == 3):      #掷骰子
            if canTurn:
                myTurn = (myTurn + 1) % playersNum
                print("player:", myTurn, end = '  ')
                if hasPathStackTop(myTurn) == 'Found':        #有棋子可走
                    steps = random.randint(1,6)
                    print("steps:", steps, end = '  ')
                    canPick =True; canTurn = False                          
                else: 
                    #steps = 0
                    print("No way!")                    
                    canPick =False; canTurn = True      #无子可走，直接下一轮掷骰子

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if canPick:
                if steps != 6:
                    mx, my = pygame.mouse.get_pos()            
                    pos = whichPos(mx, my)                    
                    if pos != 'otherPlace': 
                        if pos < 25:                                          #所选位置有效
                            if len(path[pos].stack) > 0:                      #节点上有棋子
                                if int(path[pos].gettopcid() / 4) == myTurn:  #是正确轮次的棋子
                                    print("Pick:", pos, end = '  ')
                                    qiid = path[pos].gettopcid()
                                    infoCase = moveChess()
                                    canPick =False; canTurn = True
                else:                    
                    if firstPick:
                        mx, my = pygame.mouse.get_pos()            
                        pos = whichPos(mx, my)                        
                        if pos != 'otherPlace':
                            if pos < 25:
                                if len(path[pos].stack) > 0: 
                                    if int(path[pos].gettopcid() / 4) == myTurn:   
                                        qiid = path[pos].gettopcid()
                                        firstPick = False
                                        print("one:", pos)
                    else:
                        mx, my = pygame.mouse.get_pos()            
                        pos2 = whichPos(mx, my)                         #第2次点选                   
                        if pos2 != 'otherPlace':
                            if pos2 > 3:
                                if pos < 4:                             #第1次点选                              
                                    s = pos2 - startpos         
                                else:
                                    s = pos2 - pos
                                if s > 0 and s < 7: 
                                    steps = s                                   
                                    if path[pos2].where != 'someone':                     
                                        print("two:", pos2)
                                        infoCase = moveChess()
                                        firstPick = True
                                        canPick =False; canTurn = True
                                



    screen.blit(background_image, (0,0))                #将背景图画上去
    '''
    for i in range(len(PosCenter)):
        pygame.draw.circle(screen, (255,0,0), (PosCenter[i][0], PosCenter[i][1]), 45, 1)
    #将节点圆圈画上去
    '''
    for i in range(len(path)):
        if path[i].where == 'wood':                     #放木板
            x, y = PosRect[i]
            screen.blit(pad_image, (x-5, y-5))
        for j in range(len(path[i].stack)):             #放棋子         
            color = int(path[i].stack[j].cid / 4)
            x, y = PosRect[i]                     
            screen.blit(chess_image[color], (x, y - j * 5))   


    whoWin() 
    #if steps == 0:  info_surface = infofont.render(info['start'], True, myRGB[4])
    #elif steps == 6:  info_surface = infofont.render(info['step6'], True, myRGB[4])
    
    if infoCase == 'inWater': 
        info_surface = infofont.render(info['inWater'], True, myRGB[4])
        print('In Water')
    #info_surface = infofont.render(info[infoCase], True, myRGB[4])
    screen.blit(info_surface, (320, 716))

    text_surface = font.render(str(steps), True, myRGB[myTurn])    #按轮次显示相应颜色的步数
    screen.blit(text_surface, (1007, 74))



    pygame.display.update()    #刷新一下画面
    mainClock.tick(FPS)

    '''
    if infoCase == 'inWater': info_surface = infofont.render(info['inWater'], True, myRGB[4])
    if infoCase == 'reserved':  info_surface = infofont.render(info['reserved'], True, myRGB[4])
    if infoCase == 'openBox':  info_surface = infofont.render(info['openBox'], True, myRGB[4])  
    
    if infoCase == '0win': info_surface = infofont.render(info['0win'], True, myRGB[4])
    if infoCase == '1win': info_surface = infofont.render(info['1win'], True, myRGB[4])
    if infoCase == '2win': info_surface = infofont.render(info['2win'], True, myRGB[4])
    '''

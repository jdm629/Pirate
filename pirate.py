#!/usr/bin/env python

PosCenter = ((806, 521), (855, 429), (884, 334), (882, 231), (804, 175),
            (708, 136), (619, 175), (516, 158), (415, 158), (384, 253),
            (424, 341), (490, 425), (512, 521), (446, 597), (337, 627),
            (246, 631), (159, 606), (98, 518), (139, 427), (197, 344), (237, 253), 
            (250, 130), (200, 50), (64, 64), (120, 170), (47, 263))
#各个节点的中心坐标
Pos= [ [0 for i in range(2)] for i in range(26)]
for i in range(len(PosCenter)):
    Pos[i][0]=PosCenter[i][0]-43
    Pos[i][1]=PosCenter[i][1]-43
#各个节点的左上角坐标

class Pirate:
    name = ''
    pos0 = 0
    pos1 = 0
    isActive = True
    def __init__(self, name):
        self.name = name
   # def move(pos0, pos1)


 
import pygame
#导入pygame库
from pygame.locals import *
#导入一些常用的函数和常量
from sys import exit
#向sys模块借一个exit函数用来退出程序
import math 

pygame.init()
#初始化pygame,为使用硬件做准备
FPS = 100 
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode((930, 700), 0, 32)
#创建了一个窗口
pygame.display.set_caption("小海盗")
#设置窗口标题
 
background_image = pygame.image.load('board.jpg').convert()
pad_image = pygame.image.load('pad.png').convert_alpha()
player1_image = pygame.image.load('player1.png').convert_alpha()
player2_image = pygame.image.load('player2.png').convert_alpha()
player3_image = pygame.image.load('player3.png').convert_alpha()
player4_image = pygame.image.load('player4.png').convert_alpha()
#加载并转换图像 

speed = 200
clock = pygame.time.Clock()

x, y = Pos[0]
dstx, dsty = Pos[0] 
stepx = 0; stepy = 0 
idx = 1 

while True:
#游戏主循环 
    for event in pygame.event.get():
        if event.type == QUIT:
            #接收到退出事件后退出程序
            exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            #dstx, dsty = pygame.mouse.get_pos()
            dstx, dsty = Pos[idx]
            dx = dstx - x; dy = dsty - y 
            stepx = dx/10; stepy = dy/10
            idx+=1
            if idx > 25:
                idx = 0


    screen.blit(background_image, (0,0))
    #将背景图画上去    
    for i in range(len(PosCenter)):
        pygame.draw.circle(screen, (255,0,0), (PosCenter[i][0], PosCenter[i][1]), 45, 1)
    #将节点圆圈画上去


    screen.blit(player1_image, (x, y))

    if math.fabs((x-dstx)+(y-dsty))>2:
        x += stepx; y += stepy
    else:
        x = dstx; y = dsty        


    pygame.display.update()
    #刷新一下画面
    mainClock.tick(FPS)
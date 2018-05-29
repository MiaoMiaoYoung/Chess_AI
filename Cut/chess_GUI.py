# -*- coding: utf-8 -*-

import pygame
import sys
import chess

from pygame.locals import *
from sys import exit
#棋子类的基类

#初始化pygame,为使用硬件做准备
pygame.init()
#分辨率 标志位 色深 - 三个参数含义
screen = pygame.display.set_mode((720, 720), 0, 32)

class chess_piece:
    __image_path="./image/Rook-W.png"               #当前棋子图片的路径 - 暂时的
    __piece_image=pygame.image.load(__image_path).convert_alpha()

    #定义构造函数
    def __init__(self,path):
        #获取路径
        self.__image_path = path
        #生成图像
        self.__piece_image = pygame.image.load(path).convert_alpha()
        #对图像进行大小变换
        self.__piece_image = pygame.transform.smoothscale(self.__piece_image, (self.__piece_image.get_size()[0] // 2, self.__piece_image.get_size()[1] // 2))

    #在相应的棋格打印棋子
    def draw_pieces(self,x,y,screen):
        #在现在的位置打印当前的棋子
        screen.blit(self.__piece_image, (x, y))

#def draw_pieces():



#创建了一个窗口

#设置窗口标题
pygame.display.set_caption("Chess-yang")
#设置背景
background_image_filename = './/image//chess_board.jpg'
background = pygame.image.load(background_image_filename).convert()
#获取背景位图的宽和高
bg_width,bg_height = background.get_size()
#调整背景大小
background = pygame.transform.smoothscale(background,(bg_width//4+bg_width//30,bg_height//4++bg_width//30))
# 将背景图画上去
screen.blit(background, (0, 0))

#生成棋子的图案
king_B = chess_piece('.//image//king-B.png')
king_W = chess_piece('.//image//king-W.png')
queen_B = chess_piece('.//image//queen-B.png')
queen_W = chess_piece('.//image//queen-W.png')
bishop_B = chess_piece('.//image//bishop-B.png')
bishop_W = chess_piece('.//image//bishop-W.png')
knight_B = chess_piece('.//image//knight-B.png')
knight_W = chess_piece('.//image//knight-W.png')
pawn_B = chess_piece('.//image//pawn-B.png')
pawn_W = chess_piece('.//image//pawn-W.png')
rook_B = chess_piece('.//image//rook-B.png')
rook_W = chess_piece('.//image//rook-W.png')

Pieces={'r':rook_W,'n':knight_W,'b':bishop_W,'q':queen_W,'k':king_W,'p':pawn_W,
        'R':rook_B,'N':knight_B,'B':bishop_B,'Q':queen_B,'K':king_B,'P':pawn_B}


#建立一个棋谱
board=chess.Board()
origin=66       #棋盘的起始位置 - 由当前小格得到
bias_loca=75    #棋盘每个小格的距离

board_edge_x=['a','b','c','d','e','f','g','h']
board_edge_y=['1','2','3','4','5','6','7','8']

choice_piece_start= 0, 0    #选中的棋子
start_piece_loc= 0, 0   #当前鼠标的位置

while True:

    #刷新背景
    screen.blit(background, (0, 0))

    #等待事件的发生，不加这句话的话...CPU烧的很厉害
    wait = pygame.event.wait()

    #抓取事件 - 抓取鼠标的动作，给出相应的指示
    Signal_mouse_left=False
    if wait.type == QUIT:
        exit()
    elif wait.type==MOUSEBUTTONDOWN:             #按下左键
        start_piece_loc=pygame.mouse.get_pos()
        choice_piece_start= int((start_piece_loc[1] - origin) / bias_loca), int((start_piece_loc[0] - origin) / bias_loca) #选中当前棋子的位置
        Signal_mouse_left=True
    elif wait.type==MOUSEBUTTONUP:                 #放开左键
        end_piece_loc = pygame.mouse.get_pos()     #鼠标放开的位置
        choice_piece_end = int((end_piece_loc[1] - origin) / bias_loca), int((end_piece_loc[0] - origin) / bias_loca)       #选中当前棋子落子的位置
        #棋盘上进行棋子的移动
        #生成棋子移动的路径
        Once_move=board_edge_x[choice_piece_start[1]]+board_edge_y[7-choice_piece_start[0]]+board_edge_x[choice_piece_end[1]]+board_edge_y[7-choice_piece_end[0]]
        print(Once_move)
        Piece_Move=chess.Move.from_uci(Once_move)
        if Piece_Move in board.legal_moves:
            board.push(Piece_Move)
            print(board)
        else:
            print("illegal input")

    layout_pieces = board.fen()  # 导出棋谱的当前布局
    layout = [['.' for i in range(8)] for j in range(8)]
    count = 0
    #将当前棋谱转换的好看一些
    for i in layout_pieces:
        if(count<64):
            if(i<='8' and i>='1'):
                count+=int(i)-int('0')
            elif(i!='/'):
                layout[int(count/8)][count%8]=i
                count+=1

    count = 0
    cx,cy=0,0
    for i in layout_pieces:
        # 计算当前棋格的位置
        if pygame.mouse.get_pressed()[0]==True and count == choice_piece_start[0]*8+choice_piece_start[1]:     #左键保持 并且当且棋子被选中
           cx = pygame.mouse.get_pos()[0]-(start_piece_loc[0] - choice_piece_start[1] * bias_loca - origin) #拿到鼠标的当前位置
           cy = pygame.mouse.get_pos()[1]-(start_piece_loc[1] - choice_piece_start[0] * bias_loca - origin) #拿到鼠标的当前位置
        else:
            cx = origin + (count % 8) * bias_loca - 5
            cy = origin + int(count / 8) * bias_loca - 5
        # 画棋子
        if (count < 64):
            if (i <= '8' and i >= '1'):
                count += int(i) - int('0')
            elif (i != '/'):
                Pieces[i].draw_pieces(cx,cy,screen) #通过字典映射的方式调用相应的画棋子
                count += 1


     # 刷新一下画面
    pygame.display.update()





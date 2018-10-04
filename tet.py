#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import sys
import random

blocks = (((0,4),(0,5)),((0,4),(0,5),(0,6),(0,7))
        ,((1,4),(1,5),(1,6),(0,5)),((1,4),(1,5),(1,6),(0,4)))

class Game:

    kst = 0 #キー状態
    ky = {K_RIGHT:1,K_UP:2,K_LEFT:3,K_DOWN:4,K_ESCAPE:-1,K_q:-1}
    H,W = 20,10 #ゲームのマス目サイズ
    #mv = {1:[1,0],2:[0,-1],3:[-1,0],4:[0,1]} #移動
    SCREEN_SIZE = (200, 400)
    m = 20
    md = 15

    def __init__(self):
        pygame.init();
        pygame.display.set_caption(u"TETRIS")
        self.mf = pygame.font.Font("ipag.ttf", 80)
        self.scr = pygame.display.set_mode(self.SCREEN_SIZE)
        self.hello1 = self.mf.render(u"こんにちは！", False, (0,0,0))
        self.sec = 0
        self.T = 1
        self.t = 1 
        self.k = 0 #Keyキュー
        self.state = 0 #状態
        self.blk = [[0 for i in range(self.W)] for j in range(self.H)]
        self.moveblk = [] #[y,x]

    def rmv(self):
        rvd = False
        for i,val in enumerate(self.blk):
            cnt = 0
            for j in val:
                if j == 1:
                    cnt += 1
            if cnt == self.W: #消す
                del self.blk[i]
                self.blk.insert(0,[0 for l in range(self.W)])
                rvd = True
                break
        return rvd

    def calcLRBlocks(self):
        if self.state != 1:
            return
        if self.k == 1 or self.k == 3: #左右に行けたら行く
            p = 1 if self.k == 1 else -1
            moveLR = True
            for y,x in self.moveblk:
                if x+p < 0 or x+p >= self.W:
                    moveLR = False
                    break
                if self.blk[y][x+p] == 1:
                    moveLR = False
                    break
            if moveLR:
                for i in range(len(self.moveblk)):
                    self.moveblk[i][1] += p
            #Keyキューを空に
            self.k = 0

    def calcNewBlocks(self):
        b = random.choice(blocks)
        for i in b:
            if self.blk[i[0]][i[1]] == 1:
                self.state = 2
                break
        if self.state == 2:
            for i in b:
                self.blk[i[0]][i[1]] = 1
        else:
            self.state = 1
            for i in b:
                self.moveblk.append([i[0],i[1]])

    def calcMoveBlocks(self):
        for y,x in self.moveblk:
            if y+1 >= self.H:
                self.state = 1.5
                break
            if self.blk[y+1][x] == 1:
                self.state = 1.5
                break
        if self.state == 1: #移動
            for i in range(len(self.moveblk)):
                self.moveblk[i][0] += 1
        elif self.state == 1.5: #固定
            for y,x in self.moveblk:
                self.blk[y][x] = 1
                self.moveblk = []
            while(True):
                if not self.rmv():
                    break

    def calcBlocks(self): #縦の移動・ブロック生成
        if (self.state == 0 and self.k != 0) or self.state == 1.5:
            self.calcNewBlocks()
        elif self.state == 1:
            self.calcMoveBlocks()
        elif self.state == 2 and self.k != 0:
            self.__init__()

    def calc(self):
        self.sec += 1
        if self.kst != 0: #キー記録
            self.k = self.kst

        if self.sec % self.t == 0: #tごとに処理
            self.calcLRBlocks()

        if self.sec % self.T == 0: #Tごとに処理
            self.sec = 0
            # 盤面を更新する
            self.calcBlocks()

            #Keyキューを空にする
            self.k = 0

    def drawRect(self,x,y,c):
        self.scr.fill(c,Rect(x*self.m+(self.m-self.md)/2,y*self.m+(self.m-self.md)/2,self.md,self.md));

    def draw(self):
        self.scr.fill((0,0,0))
        #self.hello1 = self.mf.render(u"%d"%self.state, False, (0,255,0))
        self.scr.blit(self.hello1, (20,50))

        for y in range(self.H):
            for x in range(self.W):
                if self.blk[y][x] == 1:
                    self.drawRect(x,y,(255,255,0))

        for i in self.moveblk:
            self.drawRect(i[1],i[0],(255,0,0))

    def event(self):
        flag = False
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key in self.ky.keys():
                    self.kst = self.ky[evt.key]
                    flag = True

            if evt.type == QUIT or self.kst == -1:
                pygame.quit()
                sys.exit()

        if not flag:
            self.kst = 0

    def main(self):
        while True:
            pygame.time.Clock().tick(60);
            self.calc();
            self.draw();
            pygame.display.update()
            self.event();

if __name__ == '__main__' :
    game = Game();
    game.main();

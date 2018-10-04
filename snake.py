#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import sys
import random

#default:(W,H,m,md,T,t,Tmin) = (16,12,40,30,30,2,10)

prm = {"W":30,"H":25,"m":25,"md":15,"T":10,"t":2,"Tmin":5,"L":100}

class Game:

    kst = 0 #キー状態
    ky = {K_RIGHT:1,K_UP:2,K_LEFT:3,K_DOWN:4,K_ESCAPE:-1,K_q:-1,K_SPACE:-2}
    W,H = prm["W"],prm["H"] #ゲームのマス目サイズ
    m = prm["m"] #マス目サイズ
    md = prm["md"] #描写マス目サイズ
    mv = {1:(1,0),2:(0,-1),3:(-1,0),4:(0,1)} #移動
    SCREEN_SIZE = (m*W, m*H)
    fst = [int(W/2),int(H/2)] #初期位置
    t,Tmin = prm["t"],prm["Tmin"] #減少値、最小周期

    def __init__(self):
        pygame.init();
        pygame.display.set_caption(u"SNAKE")
        self.scr = pygame.display.set_mode(self.SCREEN_SIZE)
        self.sec = 0
        self.T = prm["T"] #移動周期
        self.L = prm["L"] #初期長さ
        self.i,self.j = 0,0
        self.pi,self.pj = 0,0
        self.snake = [self.fst for i in range(self.L)]
        self.spc = [[i,j] for i in range(self.W) for j in range(self.H)]
        self.frt = random.choice([i for i in self.spc if i not in self.fst])
        self.start = False
        self.end = False

    def calc(self):
        self.sec += 1
        if self.kst in self.mv.keys():
            self.i,self.j = self.mv[self.kst]

        if self.end: #スコア
            if self.kst == -2:
                self.end = True
                self.__init__()
                return
            else:
                return

        if self.sec % self.T == 0:
            self.sec = 0
            #移動
            if((self.pi + self.i == 0 and self.pi != 0)
                    or (self.pj + self.j == 0 and self.pj != 0)):
                self.i,self.j = self.pi,self.pj
            x = (self.snake[0][0] + self.i) % self.W
            y = (self.snake[0][1] + self.j) % self.H
            self.snake.insert(0,[x,y])
            del self.snake[-1]
            self.pi,self.pj = self.i,self.j
            if((self.i !=0 or self.j !=0) and not self.start):
                self.start = True

            #当たり判定（開始前は判定無し）
            if self.snake[0] in self.snake[1:] and self.start:
                self.end = True

            if self.snake[0] == self.frt: #成長
                i = self.snake[-1]
                self.snake.append(i)
                self.T = max(self.Tmin,self.T-self.t)
                if len(self.snake) >= self.W*self.H: #クリア
                    self.__init__()
                self.frt = random.choice([i for i in self.spc if i not in self.snake])

    def drawRect(self,x,y,c):
        self.scr.fill(c,Rect(x*self.m+(self.m-self.md)/2,y*self.m+(self.m-self.md)/2,self.md,self.md));

    def draw(self):
        self.scr.fill((0,0,0))

        for i in self.snake[1:]:
            self.drawRect(i[0],i[1],(0,200,255))
        self.drawRect(self.snake[0][0],self.snake[0][1],(155,255,0))
        self.drawRect(self.frt[0],self.frt[1],(255,0,0))
            
    def event(self):
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key in self.ky.keys():
                    self.kst = self.ky[evt.key]
                else:
                    self.kst = 0
            else:
                self.kst = 0

            if evt.type == QUIT or self.kst == -1:
                pygame.quit()
                sys.exit()

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

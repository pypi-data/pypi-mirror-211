import pygame,sys
from pygame.locals import *
from math import *

class button:
    def __init__(self,target,font,text,color=[255,255,255],size=40,use=False,do=None):
        self.target=target
        if use:
            self.font=font
        else:
            self.font=pygame.font.SysFont(font,size)
        self.backC=[150,150,150]
        self.text=self.font.render(text,True,color)
        self.rect=self.text.get_rect()
        self.do=do
    def xyRtInit(self,x,y):
        self.rect.x=x
        self.rect.y=y
        return self
    def WhereRtInit(self,wh,x=0,y=0):
        if wh==0:
            self.rect.x=0+x
            self.rect.y=0+y
        elif wh == 1:
            self.rect.x=self.target.get_size()[0]-self.rect.w+x
            self.rect.y=0+y
        elif wh == 2:
            self.rect.x=0+x
            self.rect.y=self.target.get_size()[1]-self.rect.h+y
        elif wh == 3:
            self.rect.x=self.target.get_size()[0]-self.rect.w+x
            self.rect.y=self.target.get_size()[1]-self.rect.h+y
        elif wh == 4:
            self.rect.x=(self.target.get_size()[0]-self.rect.w)/2+x
            self.rect.y=(self.target.get_size()[1]-self.rect.h)/2+y

        return self
    def absJump(self,x,y):
        self.rect.x+=x
        self.rect.y+=y
    def Where(self,wh):
        if wh==0:
            self.rect.x=0+x
            self.rect.y=0+y
        elif wh == 1:
            self.rect.x=self.target.get_size()[0]-self.rect.w+x
            self.rect.y=0+y
        elif wh == 2:
            self.rect.x=0+x
            self.rect.y=self.target.get_size()[1]-self.rect.h+y
        elif wh == 3:
            self.rect.x=self.target.get_size()[0]-self.rect.w+x
            self.rect.y=self.target.get_size()[1]-self.rect.h+y
        elif wh == 4:
            self.rect.x=(self.target.get_size()[0]-self.rect.w)/2+x
            self.rect.y=(self.target.get_size()[1]-self.rect.h)/2+y

    def xy(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def change(self,font,text,color=[255,255,255],size=40,use=False):
        if use:
            self.font=font
        else:
            self.font=pygame.font.SysFont(font,size)
        self.text=self.font.render(text,True,color)
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        if self.rect.collidepoint(pygame.mouse.get_pos())\
           and mouseDown:
            self.do()
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.target,self.backC,self.rect)
        self.target.blit(self.text,self.rect)


import pygame,sys
from pygame.locals import *
from math import *

class image:
    def __init__(self,target,file,w=0,h=0):
        self.target=target
        if w == 0 and h == 0:
            self.img = pygame.image.load(file)
        else:
            self.img = pygame.transform.scale(pygame.image.load(file),(w,h))
        self.rect=self.img.get_rect()
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
    def change(self,file):
        self.img=pygame.image.load(file)
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        self.target.blit(self.img,self.rect)

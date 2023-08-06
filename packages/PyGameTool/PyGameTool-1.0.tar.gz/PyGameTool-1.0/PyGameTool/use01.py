print('''

import pygame,sys
from pyg import *
from pygame.locals import *
from math import *
from create import *

pygame.init()

class FightSq(image):
    def __init__(self,target,w=0,h=0,lw=1):
        self.target=target
        mask_surface = pygame.Surface((w,h), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))

        rect_alpha = 255
        rect_color = (255, 255, 255, rect_alpha)
        rect_thickness = lw
        rect = pygame.Rect(0,0,w,h)
        pygame.draw.rect(mask_surface, rect_color, rect, rect_thickness)

        # 获取遮罩(MASK)
        self.mask = pygame.mask.from_surface(mask_surface)

        self.img=mask_surface
        
        self.rect=self.img.get_rect()
    def xy(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def change(self,w=0,h=0,lw=1):
        mask_surface = pygame.Surface((w,h), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))

        rect_alpha = 255
        rect_color = (255, 255, 255, rect_alpha)
        rect_thickness = lw
        rect = pygame.Rect(0,0,w,h)
        pygame.draw.rect(mask_surface, rect_color, rect, rect_thickness)

        # 获取遮罩(MASK)
        self.mask = pygame.mask.from_surface(mask_surface)

        self.img=mask_surface
        
        self.rect=self.img.get_rect()
    def xyRtInit(self,x,y):
        self.rect.x=x
        self.rect.y=y
        return self
    def WhereRtInit(self,wh,x=0,y=0):
        if wh==0:
            self.rect.x=0
            self.rect.y=0
        elif wh == 1:
            self.rect.x=self.target.get_size()[0]-self.rect.w
            self.rect.y=0
        elif wh == 2:
            self.rect.x=0
            self.rect.y=self.target.get_size()[1]-self.rect.h
        elif wh == 3:
            self.rect.x=self.target.get_size()[0]-self.rect.w
            self.rect.y=self.target.get_size()[1]-self.rect.h
        elif wh == 4:
            self.rect.x=(self.target.get_size()[0]-self.rect.w)/2+x
            self.rect.y=(self.target.get_size()[1]-self.rect.h)/2+y

        return self
    def Where(self,wh):
        if wh==0:
            self.rect.x=0
            self.rect.y=0
        elif wh == 1:
            self.rect.x=self.target.get_size()[0]-self.rect.w
            self.rect.y=0
        elif wh == 2:
            self.rect.x=0
            self.rect.y=self.target.get_size()[1]-self.rect.h
        elif wh == 3:
            self.rect.x=self.target.get_size()[0]-self.rect.w
            self.rect.y=self.target.get_size()[1]-self.rect.h
        elif wh == 4:
            self.rect.x=(self.target.get_size()[0]-self.rect.w)/2
            self.rect.y=(self.target.get_size()[1]-self.rect.h)/2
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        self.target.blit(self.img,self.rect)

class BOME_R(image):
    def __init__(self,target,h):
        self.target=target
        self.w=8
        self.h=h
        mask_surface = pygame.Surface((self.w,self.h), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))
        rect_alpha = 255
        rect_color = (255, 255, 255, rect_alpha)
        rect = pygame.Rect(0,0,self.w,self.h)
        pygame.draw.rect(mask_surface, rect_color, rect)
        self.img=mask_surface
        self.rect=self.img.get_rect()
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        super().upd(NOW,lists,lens,event,mouseDown)
class BOME(image):
    def __init__(self,target,speed,h,x=0,y=0,ud=0,khp=1):
        self.khp=khp
        self.SELFIS='BOME'
        super().__init__(target,'./bome.png',18,10)
        #print(self.img,x,y)
        self.rect.x=x
        self.rect.y=y
        self.bh=h
        self.w=18
        self.h=10
        self.bome_r=BOME_R(target,self.bh)
        self.bome_r.rect.x=x+5
        if ud==0:
            self.bome_r.rect.y=y+10
        elif ud==1:
            self.img=pygame.transform.rotate(self.img,180)
            self.bome_r.rect.y=y-h
        #print(self.bome_r.rect)
        self.speed=speed

        
        
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        self.rect.x+=self.speed
        self.bome_r.rect.x+=self.speed
        if self.rect.x>=self.target.get_size()[0] or self.rect.x+self.w<=0:
            lists.waitDel(lens)
        super().upd(NOW,lists,lens,event,mouseDown)
        self.bome_r.upd()

class tBOME(BOME):
    def __init__(self,target,speed,h,x=0,y=0,khp=1):
        super().__init__(target,speed,h,x,y,0,khp)
        self.SELFIS="tBOME"
        self.bome2=pygame.image.load("./bome.png")
        self.bome2=pygame.transform.rotate(self.bome2,180)
        self.rect2=self.bome2.get_rect()
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        super().upd(NOW,lists,lens,event,mouseDown)
        self.rect2.y=self.rect.y+self.h+self.bh
        self.rect2.x=self.rect.x
        self.target.blit(self.bome2,self.rect2)

"""in the create.py       
class CREATE_BOME:
    def __init__(self,target,time,maxtime,sp,bsp,h,x,y,ud,khp):
        self.target=target
        self.x=x
        self.y=y
        self.ud=ud
        self.khp=khp
        self.h=h
        self.maxtime=maxtime
        self.time=time
        self.t=0
        self.sp=sp
        self.isp=0
        self.bsp=bsp
        self.go=False
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        self.t+=1
        if self.t>=self.time and self.t<=self.maxtime:
            self.isp=(self.isp+1)%self.sp
            if self.isp == 0:
                Killer.append(BOME(self.target,self.bsp,self.h,self.x,self.y,
                                   self.ud,self.khp))"""
            

class CLASS_OF_LOVE_HP:
    def __init__(self,target,PL):
        self.PL=PL
        self.target=target
        self.xy=self.target.get_size()[0]/2-100,self.target.get_size()[1]/2+300
        self.font=pygame.font.SysFont(None,30)
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        pygame.draw.rect(self.target,(255,215,0),(*self.xy,self.PL.HP*4/2,30))
        print_on(self.target,self.font,str(int(self.PL.HP))+'/'+str(self.PL.MAX_HP),(self.xy[0]+60,self.xy[1]+50))
class CLASS_OF_LOVE(image):
    def __init__(self,target,w=0,h=0):
        super().__init__(target,'./Love.png',w,h)
        self.speed=6
        self.NOW_IS=0
        self.HP=92
        self.MAX_HP=92
        self.THP=92
        self.killerRect=self.rect.copy()
        self.killerRect.inflate_ip(-6,-6)
        print(self.killerRect)
        self.killerRect.x=self.rect.x+3
        self.killerRect.y=self.rect.y+3
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        if event[pygame.K_f]:
            self.HP+=50
        if event[pygame.K_LEFT]:
            self.rect.x-=self.speed
        if event[pygame.K_RIGHT]:
            self.rect.x+=self.speed
        if event[pygame.K_UP]:
            self.rect.y-=self.speed
        if event[pygame.K_DOWN]:
            self.rect.y+=self.speed
        if self.rect.x<FIGHTSQ.rect.x+10:
            self.rect.x=FIGHTSQ.rect.x+10
        elif self.rect.x+16>FIGHTSQ.rect.x+490:
            self.rect.x=FIGHTSQ.rect.x+490-16
        if self.rect.y<FIGHTSQ.rect.y+10:
            self.rect.y=FIGHTSQ.rect.y+10
        elif self.rect.y+16>FIGHTSQ.rect.y+290:
            self.rect.y=FIGHTSQ.rect.y+290-16
        super().upd(NOW,lists,lens,event,mouseDown)
        self.killerRect.x=self.rect.x+3
        self.killerRect.y=self.rect.y+3
        for i in Killer.list:
            if i.SELFIS=='BOME':
                if self.killerRect.colliderect(i) or \
                   self.killerRect.colliderect(i.bome_r):
                    self.HP-=i.khp
            if i.SELFIS=='tBOME':
                if self.killerRect.colliderect(i) or \
                   self.killerRect.colliderect(i.bome_r) or \
                   self.killerRect.colliderect(i.rect2):
                    self.HP-=i.khp
        #pygame.draw.rect(self.target,(0,0,0),self.killerRect)
                    

def BUTTON_EVENT_MAINPLAY():
    global NOW
    NOW = 'play'


def print_on(target,font,text,xy,color=(255,255,255)):
    get=font.render(text,True,color)
    target.blit(get,xy)


WIN_W=1000
WIN_Y=800
win=pygame.display.set_mode((1000,800),0,32)
timer=pygame.time.Clock()

font = pygame.font.SysFont(None,50)

Love=CLASS_OF_LOVE(win,16,16).WhereRtInit(4,y=100)#Love load image
Loves=school('play')
Loves.add(Love,CLASS_OF_LOVE_HP(win,Love))


Killer=school('play')


GUI=school(None)
NOW='main'
MAIN=school('main')
PLAY=school('play')

PLAY.add(CREATE_BOME(win,0,500,3,7,300,-10,450,0,1,Killer),
         CREATE_tBOME(win,0,500,20,7,25,-10,360,1,Killer),
         CREATE_tBOME(win,10,500,20,7,25,-10,395,1,Killer))#killer


FIGHTSQ=FightSq(win,500,300,10).WhereRtInit(4,0,100)
PLAY.add(Loves,FIGHTSQ,
         Killer)
MAIN.add(button(win,None,'play',size=100,do=BUTTON_EVENT_MAINPLAY).WhereRtInit(4))
GUI.add(MAIN,PLAY)

while True:
    timer.tick(30)
    keyGet = pygame.key.get_pressed()
    mouseDown = False
    #timer.tick_busy_loop(60)
    win.fill((0,0,0))
    key = pygame.key.get_pressed()
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif i.type ==  MOUSEBUTTONDOWN:
            mouseDown=True
    GUI.upd(NOW,event=keyGet,mouseDown=mouseDown)
    print_on(win,font,str(int(timer.get_fps())),(0,0))
    pygame.display.update()


''')

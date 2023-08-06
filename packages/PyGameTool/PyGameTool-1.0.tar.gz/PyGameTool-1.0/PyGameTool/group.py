class school:
    def __init__(self,updNeed):
        self.updNeed=updNeed
        self.list=[]
        self.lenses = []
    def updnd(self,NOW,event,mouseDown):
        self.lenses.sort()
        dels=0
        for i in self.lenses:
            del self.list[i-dels]
            dels+=1
        self.lenses=[]
        for i in range(len(self.list)):
            self.list[i].upd(NOW,self,i,event,mouseDown)
        
    def upd(self,NOW=None,lists=None,lens=None,event=None,mouseDown=False):
        if self.updNeed==None:
            self.updnd(NOW,event,mouseDown)
        elif self.updNeed==NOW:
            self.updnd(NOW,event,mouseDown)
        #print(self.updNeed,NOW)
    def append(self,ob):
        self.list.append(ob)
    def waitDel(self,lens):
        self.lenses.append(lens)
    def add(self,*ob):
        for i in ob:
            self.list.append(i)

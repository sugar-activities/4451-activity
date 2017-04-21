# jigsaw.py
import g,pygame,random,utils

rc=[(2,3),(3,4),(4,5),(5,6)]
locations=[]
pieces=[]

class Location:
    def __init__(self,x,y,r,c): # ind refers to the subsurface currently there
        self.x=x; self.y=y; self.r=r; self.c=c; self.ind=len(locations)

class Jigsaw:
    def __init__(self):
        self.w=g.sy(32); self.h=g.sy(22); self.w2=self.w/2; self.h2=self.h/2
        self.screen=pygame.Surface((self.w,self.h))
        self.pic_n=1
        self.rc_n=0
        self.moving=True
        self.orange=None
        self.edge1,self.edge2=g.sy(.4),g.sy(.2) # for green & white rects
        self.grid2=make_grid(2,2,self.w/2,self.h/2,utils.WHITE,self.edge2)

    def setup_pic(self):
        pic=str(self.pic_n)+'.jpg'
        self.img1=utils.load_image(pic)
        self.img2=pygame.transform.flip(self.img1,True,False)
        self.img3=pygame.transform.flip(self.img1,True,True)
        self.img4=pygame.transform.flip(self.img1,False,True)

    def setup_pieces(self):
        global locations, pieces
        self.nr,self.nc=rc[self.rc_n]
        dx=self.w/self.nc; dy=self.h/self.nr
        locations=[]; pieces=[]
        y=0
        for r in range(self.nr):
            x=0
            for c in range(self.nc):
                loc=Location(x,y,r,c); locations.append(loc)
                piece=self.screen.subsurface((x,y,dx,dy)); pieces.append(piece)
                x+=dx
            y+=dy
        self.gw=dx; self.gh=dy # for piece
        self.grid=make_grid(self.nr,self.nc,dx,dy,utils.WHITE,g.sy(.1))

    def setup(self):
        self.setup_pic()
        self.setup_pieces()
        self.reset()

    def reset(self):
        # for movement
        self.x=random.randint(0,self.w2-1); self.y=random.randint(0,self.h2-1)
        self.dx=5; self.dy=self.dx
        for i in range(100):
            self.finished=False
            shuffle()
            if not self.complete(): break
        self.green=None # locn
        self.finished=False
        self.whole=False
        self.moving=True
        self.ms=pygame.time.get_ticks()

    def draw(self):
        x=self.x; y=self.y; w=self.w; h=self.h; w2=self.w2; h2=self.h2
        self.screen.blit(self.img1,(0,0),(x,y,w2,h2))
        self.screen.blit(self.img2,(w2,0),(w-x-w2,y,w2,h2))
        self.screen.blit(self.img4,(0,h2),(x,h-y-h2,w2,h2))
        self.screen.blit(self.img3,(w2,h2),(w-x-w2,h-y-h2,w2,h2))
        if self.whole:
            g.screen.blit(self.img1,(0,0))
            pygame.draw.rect(g.screen,utils.WHITE,\
                             (self.x,self.y,self.w2,self.h2),self.edge2)
        else:
            for locn in locations:
                g.screen.blit(pieces[locn.ind],(locn.x,locn.y))
            if not self.complete():
                g.screen.blit(self.grid,(0,0))
                if self.green!=None:
                    pygame.draw.rect(g.screen,utils.GREEN,\
                        (self.green.x,self.green.y,self.gw,self.gh),self.edge1)

    def update(self):
        if not self.moving: return
        ms=pygame.time.get_ticks()
        if ms-self.ms>200:
            self.x+=self.dx
            if self.x>self.w2:
                self.x=self.w2-random.randint(0,5); self.dx=-self.dx
            if self.x<0:
                self.x=0; self.dx=-self.dx
            self.y+=self.dy
            if self.y>self.h2:
                self.y=self.h2-random.randint(0,5); self.dy=-self.dy
            if self.y<0:
                self.y=0; self.dy=-self.dy
            self.ms=ms; g.redraw=True

    def click(self):
        if self.complete(): self.whole=not self.whole; return
        ind=0
        for locn in locations:
            if utils.mouse_in(locn.x,locn.y,locn.x+self.gw,locn.y+self.gh):
                if ind==0: return False
                if self.green==None:
                    self.green=locn
                else:
                    if self.green==locn:
                        self.green=None
                    else:
                        t=locn.ind; locn.ind=self.green.ind; self.green.ind=t
                        self.green=None
                return True
            ind+=1
        return False

    def check_mouse(self):
        ind=0
        for locn in locations:
            if utils.mouse_in(locn.x,locn.y,locn.x+self.gw,locn.y+self.gh):
                if ind==0:
                    self.orange=locations[1]
                else:
                    self.orange=locn
                return
            ind+=1
        
    def locn(self,r0,c0):
        ind=0
        for r in range(self.nr):
            for c in range(self.nc):
                if r==r0 and c==c0: return locations[ind]
                ind+=1
        return None

    def orange_set(self):
        if self.orange==None: self.orange=locations[1]
        x=self.orange.x+self.gw/2; y=self.orange.y+self.gh/2
        pygame.mouse.set_pos((x,y)); g.pos=(x,y)
        
    def inc_r(self):
        if self.orange==None: self.orange=locations[1]; return
        r=self.orange.r; c=self.orange.c
        r+=1
        if r==self.nr:
            r=0
            if c==0: r=1
        self.orange=self.locn(r,c); self.orange_set()
        
    def dec_r(self):
        if self.orange==None: self.orange=locations[1]; return
        r=self.orange.r; c=self.orange.c
        r-=1
        if r<0:
            r=self.nr-1
        if r==0 and c==0: r=self.nr-1
        self.orange=self.locn(r,c); self.orange_set()
        
    def inc_c(self):
        if self.orange==None: self.orange=locations[1]; return
        r=self.orange.r; c=self.orange.c
        c+=1
        if c==self.nc:
            c=0
            if r==0: c=1
        self.orange=self.locn(r,c); self.orange_set()
        
    def dec_c(self):
        if self.orange==None: self.orange=locations[1]; return
        r=self.orange.r; c=self.orange.c
        c-=1
        if c<0:
            c=self.nc-1
        if r==0 and c==0: c=self.nc-1
        self.orange=self.locn(r,c); self.orange_set()
        
    def complete(self):
        if self.finished: return True
        ind=0
        for locn in locations:
            if locn.ind!=ind: return False
            ind+=1
        self.finished=True
        return True
        
def shuffle():
    ln=len(locations)
    for i in range(500):
        r1=random.randint(1,ln-1); r2=random.randint(1,ln-1)
        locations[r1].ind,locations[r2].ind=locations[r2].ind,locations[r1].ind

def make_grid(nr,nc,dx,dy,colr,px=1): # returns surface
    w=nc*dx; h=nr*dy
    surf=pygame.Surface((w,h))
    surf.set_colorkey((0,0,0))
    x1=0; x2=x1+w; y=0
    for r in range(nr+1):
        pygame.draw.line(surf,colr,(x1,y),(x2,y),px)
        y+=dy
    x=0; y1=0; y2=y1+h
    for c in range(nc+1):
        pygame.draw.line(surf,colr,(x,y1),(x,y2),px)
        x+=dx
    return surf
        
            

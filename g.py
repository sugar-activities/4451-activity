# g.py - globals
import pygame,utils,random,os

app='PMJ'; ver='1.0'
ver='1.1'
# tablet version
ver='1.2'
# retain mouse position if set via orange_set()
ver='1.3'
# allow arrows on XO, Enter=tick
ver='1.4'
# orange rect on menu - mouse follows arrows
ver='1.5'
# fake cursor
ver='1.6'
# title centred
ver='1.8'
# rectangle sizes scaled
# negative pointer
ver='2.0'
# intervening versions scrapped - sluggish problem
# remove pixel reduction in make_grid
# finale change -
#  left click toggles between kaleid and whole via jigsaw.whole variable
ver='2.1'
# x key works in finale
# new key constants
ver='2.2'
# position pointer at start of jigsaw
# new title
ver='21'
ver='22'
# flush_queue() doesn't use gtk on non-XO

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer,negative
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((255,255,192))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(60*imgf); font1=pygame.font.Font(None,t)
        t=int(80*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    negative=utils.load_image('negative.png',True)
    
    # this activity only
    global level,best,title,title_c,star,state
    level=1
    best=[]
    for ind in range(12): best.append(0)
    title=utils.load_image('title.png',True)
    title_c=w/2,title.get_height()/2
    star=utils.load_image('star.png',True)
    state=1
    # 1 title
    # 2 menu
    # 3 jigsaw
    
def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)

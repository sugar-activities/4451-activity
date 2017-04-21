#!/usr/bin/python
# PMJ.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,buttons,slider,load_save,jigsaw,menu
try:
    import gtk
except:
    pass

class PMJ:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill((255,255,192))
        if g.state==1:
            utils.centre_blit(g.screen,g.title,g.title_c)
        elif g.state==2:
            g.title=None
            self.menu.draw()
            self.slider.draw()
        elif g.state==3:
            self.jigsaw.draw()
        buttons.draw()

    def buttons_setup(self):
        buttons.Button('new',(g.sx(16),g.sy(20.8)))

    def do_click(self):
        if g.state==2: # menu
            if self.slider.mouse(): return # level changed
            n=self.menu.orange.n
            self.jigsaw.pic_n=n
            self.jigsaw.rc_n=g.level-1
            self.jigsaw.setup()
            self.jigsaw.orange=None; self.jigsaw.orange_set()
            g.state=3
        elif g.state==3: # jigsaw
            self.jigsaw.click()
            if self.jigsaw.complete(): buttons.on('new')

    def do_button(self,bu):
        if bu=='new':
            if g.state==3:
                if self.jigsaw.complete():
                    n=self.jigsaw.pic_n
                    if g.level>g.best[n-1]: g.best[n-1]=g.level
            g.state=2; buttons.off('new')
            self.menu.orange=None; self.menu.orange_set()

    def do_key(self,key):
        if key in g.SQUARE: self.do_button('new'); return
        if g.state==2: # menu
            if key in g.DOWN: self.menu.inc_r(); return
            if key in g.UP: self.menu.dec_r(); return
            if key in g.RIGHT: self.menu.inc_c(); return
            if key in g.LEFT: self.menu.dec_c(); return
            if key in g.CROSS: self.do_click(); return
            if key in g.TICK: self.inc_level()
        if g.state==3: # jigsaw
            if not self.jigsaw.complete():
                if key in g.DOWN: self.jigsaw.inc_r(); return
                if key in g.UP: self.jigsaw.dec_r(); return
                if key in g.RIGHT: self.jigsaw.inc_c(); return
                if key in g.LEFT: self.jigsaw.dec_c(); return
            if key in g.CROSS: self.do_click(); return
            if key in g.CIRCLE:
                self.jigsaw.moving=not self.jigsaw.moving; return
        if key==pygame.K_v: g.version_display=not g.version_display; return

    def inc_level(self):
        g.level+=1
        if g.level>self.slider.steps: g.level=1
        self.jigsaw.rc_n=g.level-1
        self.jigsaw.setup()
        self.jigsaw.orange=None

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        self.jigsaw=jigsaw.Jigsaw()
        self.menu=menu.Menu(3,4,g.sy(1),g.sy(1.5),g.sy(.32))
        load_save.retrieve()
        self.buttons_setup()
        self.slider=slider.Slider(g.sx(16),g.sy(20.5),len(jigsaw.rc),utils.GREEN)
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    if g.state==2: self.menu.check_mouse()
                    if g.state==3: self.jigsaw.check_mouse()
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        bu=buttons.check()
                        if bu!='': self.do_button(bu)
                        else: self.do_click()
                    if event.button==3:
                        self.jigsaw.moving=not self.jigsaw.moving
                    self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.state==3:
                self.jigsaw.update()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                if g.state==3:
                    g.screen.blit(g.negative,g.pos)
                else:
                    g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=PMJ()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)

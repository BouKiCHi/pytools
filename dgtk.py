#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# dgTK Copyright (C) 2012,2013 by BouKiCHi
#
# dgTK is a Portable GUI ToolKik
#
# Version 1.0 2013-03-17
# * Use pygame internal keyrepeat function instead of self written.
# * Did refactoring
# * Added drawbox function
# * Changed default colors
#

# The code is provided under the MIT License
#
# Please see the below URL for the detail
# http://opensource.org/licenses/mit-license.php
#

import os
import pygame
import re
import pprint

#
# Global variables
#

START  = pygame.K_RETURN
SELECT = pygame.K_ESCAPE
L = pygame.K_TAB
R = pygame.K_BACKSPACE
X = pygame.K_SPACE
Y = pygame.K_LSHIFT
A = pygame.K_LCTRL
B = pygame.K_LALT
DOWN = pygame.K_DOWN
UP = pygame.K_UP
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

CANCEL = -1


color = {
'black':(0,0,0),
'white':(255,255,255),
'red':(255,0,0),
'darkred':(64,0,0),
'green':(0,255,0),
'darkgreen':(0,64,0),
'blue':(0,0,255),
'darkblue':(0,0,64),
'lightblue':(0,255,255),
'purple':(255,0,255),
'yellow':(255,255,0),
'darkgray':(64,64,64),
'lightgray':(192,192,192),
'shadow':(0,0,0)
}


#
# Basic functions
#

def get_string_size(msg, name="m"):
    f = font[name]
    return f.size(msg)


def init(screen_surface):
    global screen    
    screen = screen_surface

    load_fonts()

def load_fonts():
    global font
    
    font = {
        "s" : pygame.font.SysFont("None", 16),
        "m" : pygame.font.SysFont("None", 24),
        "l" : pygame.font.SysFont("None", 48)
        }


def load_unifonts(filename):
    global font
    
    if not os.path.exists(filename):
        return
   
    font = {
        "s" : pygame.font.Font(filename, 16),
        "m" : pygame.font.Font(filename, 20),
        "l" : pygame.font.Font(filename, 40)
        }


def load_font(name, filename, size):

    fontpath = None

    path = os.path.join(get_sysfont_dir(), filename)

    if os.path.exists(path):
        fontpath = path

    path = os.path.join(get_localfont_dir(), filename)

    if os.path.exists(path):
        fontpath = path

    path = os.path.join(get_userfont_dir(), filename)

    if os.path.exists(path):
        fontpath = path
    
    if fontpath is not None:
        font[name]=pygame.font.Font(fontpath, size)
        return True

    return False

#
# Utilities
#

def get_homefilepath(name):
    return os.path.expanduser("~/"+name)

def get_sysfont_dir():
    return "/usr/local/share/fonts/"

def get_localfont_dir():
    return os.path.expanduser("~/.fonts/")

def get_userfont_dir():
    return "fonts/"

def get_default_cjk_font():
    return "DroidSansFallback.ttf"

    
#
# Count class
#

class dgCount:
    def __init__(self, pos=0, min=0, max=100, step=1, loop=False):

        self.pos = pos
        self.min = min
        
        self.set_max(max)
        
        if self.pos > self.max:
            self.pos = self.max

        if self.pos < self.min:
            self.pos = self.min
        
        self.step = step
        self.loop = loop
    
    def set_max(self, max):

        if max < 0:
            max = 0
        
        if self.pos > max:
            self.pos = max

        self.max = max


    def inc(self):

        if self.pos < self.max:
            self.pos += 1
        else:
            if self.loop:
                self.pos = 0
            else:
                self.pos = self.max
                return True
        
        return False

    def dec(self):

        if self.pos > 0:
            self.pos -= 1
        else:
            if self.loop:
                self.pos = self.max
            else:
                self.pos = 0
                return True
                
        return False

    
    def add(self, num, max=False):

        if self.pos + num <= self.max:
            self.pos += num
        else:
            if self.loop:
                self.pos = self.pos + num - self.max
            else:
                if max:
                    self.pos = self.max
                return True
                            
        return False

    
    def sub(self, num, min=False):

        if self.pos - num >= 0:
            self.pos -= num
        else:
            if self.loop:
                self.pos = self.pos - num + self.max
            else:
                if min:
                    self.pos = 0
                return True
        
        return False
    
    def set_pos(self, pos):
        self.pos = pos
    
    def get_pos(self):
        return self.pos


#
# dgUI primitive class
#

class dgUI:

    def __init__(self, scrn, appname="DGTK UI", appconf="dgtk_user.cfg"):
        
        self.scrn = scrn
        self.sw = scrn.get_width()
        self.sh = scrn.get_height()
        self.update = True
        self.title_h = 10
        self.delay_ms = 10
        self.shadow = True
        self.sysconf_name = "dgtk.cfg"
        self.appconf_name = appconf
        
        pygame.key.set_repeat(200, 50)

        self.set_caption(appname)
        self.set_config()

    def set_config(self):

        self.conf = {}
        self.conf["color"] = {}
        
        self.conf["color"]['select'] = color['yellow']
        self.conf["color"]['background'] = color['darkblue']
        self.conf["color"]['textcolor'] = color['white']
        self.conf["color"]['shadow'] = color['darkgray']
        
        dict = self.read_config(self.sysconf_name)
		
        if dict is not None:
            self.conf.update(dict)
        
        self.appconf = self.read_config(self.appconf_name)


    def read_config(self, name):

        path = get_homefilepath("." + name)
		
        if os.path.exists(path):

            f = open(path, "r")
            text = f.read()
            f.close()
            dict = eval(text)
            return dict

        return None
        
   
    def write_config(self, name, dict):
	
        path = get_homefilepath("." + name)
        
        f = open(path, "w")
        pprint.pprint(dict, f)
        f.close()

    
    def set_caption(self, name):
        self.caption = name
        
    def build_line(self, l_chrs, w, h):

        x = 0
        y = 0
        
        flags = l_chrs[0].get_flags()
        dst = pygame.Surface((w, h), flags)
        
        for s in l_chrs:
            w, h = s.get_size()                
            dst.blit(s, (x, y))
            x += w
        
        return dst

    def render_string_lines(self, msg, c, cs, name="m", shadow=True):

        sw, sh = self.scrn.get_size()

        anti = True

        x = 0
        w = 0
        lh = 0

        f = font[name]
        l_lines = []
        l_chrs = []
        
        if len(msg)==0:
            s = f.render(" ", anti, c)
            cw, ch = s.get_size()
            return [self.build_line([s], cw, ch)]
            
        for chr in msg:

            s = f.render(chr, anti, c)
            cw, ch = s.get_size()
            
            # next line
            if x + cw >= sw:

                l_lines.append(self.build_line(l_chrs, w, lh))
                l_chrs = []
                lh = 0
                x = 0
                w = 0
            
            # line size
            if lh < ch:
                lh = ch

            l_chrs.append( s )

            x += cw

            if w < x:
                w = x

        if w > 0:
            l_lines.append(self.build_line(l_chrs, w, lh))

        return l_lines

    def draw_box(self, x, y, w, h, c, cs = None, msg = None, name = "s"):
        if cs:
            rect = pygame.Rect(x+1, y+1, w, h)
            pygame.draw.rect(self.scrn, cs, rect, 1)

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.scrn, c, rect, 1)
        
        
        if msg is not None:
            
            s, ss = self.render_string(msg, c, cs, name=name)
            
            if ss:
                self.draw_image(ss, 1+x+(w/2), 1+y+h-ss.get_height(),x_center = True)

            self.draw_image(s, x+(w/2), y+h-ss.get_height(),x_center = True)


    def draw_image(self, obj, x, y, x_center=False, y_center=False):

        w,h = obj.get_size()
        
        if x_center:
            x -= w / 2
        if y_center:
            y -= h / 2

        self.scrn.blit(obj, (x, y))


    def render_string(self, msg, c, cs=None, name="m",shadow = True):
        shadow_surf = None

        f = font[name]

        if shadow and cs:
            shadow_surf = f.render(msg, True, cs)

        surf = f.render(msg, True, c)
        
        return (surf,shadow_surf)
        
        
    def draw_string(self, msg, x, y, c, cs=None, center=False, name="m", shadow=True):
    
        sw, sh = self.scrn.get_size()
        
        s, ss = self.render_string(msg, c, cs, name, shadow)
        
        if center:
            w,h = s.get_size()
            
            x -= w / 2
            y -= h / 2
        
        if ss:
            self.scrn.blit(ss, (x+1,y+1))
    
        self.scrn.blit(s, (x,y))
        
        return s, ss

    def draw_multi(self, msg, x, y, c, cs, center=False, name="m", shadow=True):
        f = font[name]
        
        # splits string
        
        msgs = msg.split('\n')
        
        sl = []
        h = 0
        
        # rendering
        
        for line in msgs:
            s = f.render( line, True , c )
            ss = f.render( line, True , cs )
            h += s.get_height()
            sl.append( ( s,ss ) )
        
        if center:
            y -= h / 2
        
        for st in sl:
            dx = x
            if center:
                dx = x - st[0].get_width() / 2
            
            if shadow:
                self.scrn.blit( st[1] , (dx + 1 , y + 1 ) )
            self.scrn.blit( st[0] , ( dx , y ) )
            
            y += st[0].get_height()

    
    def base_screen( self ):
        f = font['s']
        bg = self.conf["color"]["background"]
        c = self.conf["color"]["textcolor"]
        screen.fill(bg)
        screen.blit(f.render(self.caption, True, c),(0, 0))
    
    def draw(self):
        pass
    
    def keydown( self , e ):
        if e.key == SELECT:
            return True
        return False
    
    def keyup ( self , e ):
        return False
        
    def event( self , e ):
        if e.type == pygame.QUIT:
            return True
        if e.type == pygame.KEYDOWN:
            if self.keydown ( e ):
                return True
        
        if e.type == pygame.KEYUP:
            if self.keyup ( e ):
                return True
        
        return False

    def process( self ):
    
        if self.update:
            self.draw()
            pygame.display.update()
            self.update = False

        pygame.time.delay( self.delay_ms )

    def loop( self ):
        done = False
    
        while not done:
            for e in pygame.event.get():
                done = self.event( e )
                if done:
                    return
                
            self.process()


    

#
# class dgUIChoose
#
class dgUIChoose( dgUI ):

    # init

    def __init__(self, scrn, msg, opts, appname="CHOOSE"):

        dgUI.__init__(self, scrn, appname)
        self.msg = msg
        self.opts = opts
        self.count = dgCount(max = len(opts) - 1, loop = True)
        self.result = CANCEL

    # keycheck
        
    def keydown(self, e):
        self.update = True
        if e.key == SELECT:
            return True

        if e.key == LEFT:
            self.count.dec()

        if e.key == RIGHT:
            self.count.inc()
            
        if e.key == START:
            self.result = self.count.pos
            return True
        
        return False
    
                    
    def draw(self):
        sw = self.sw
        sh = self.sh
        
        c = self.conf["color"]["textcolor"]
        cs = self.conf["color"]["shadow"]
        csel = self.conf["color"]["select"]

        self.base_screen()
        self.draw_multi(self.msg, sw / 2, sh / 2, c, cs,
            True, shadow=self.shadow)
        
        l = len (self.opts)
        
        w = sw / l
        x = (w / 2)
        y = sh - (sh / 4)

        
        for i in range(l):
            if self.count.pos == i:
                self.draw_string(
                    "[%s]" % self.opts[i], x, y, csel, cs,
                    center = True , shadow = self.shadow )
            else:
                self.draw_string(
                    self.opts[i], x, y, c, cs,
                    center = True , shadow = self.shadow )
            
            x += w

#
# class dgUIYesNoChoose
#
class dgUIYesNoChoose(dgUIChoose):

    def __init__(self, scrn, msg, appname="YES/NO"):
        dgUIChoose.__init__(self, scrn, msg,["NO","YES"],appname)

#
# class dgUIOKChoose
#
class dgUIOKChoose(dgUIChoose):

    def __init__(self, scrn, msg,appname="OK?"):
        dgUIChoose.__init__(self, scrn, msg,["CANCEL","OK"],appname)


#
# class dgUIAlert
#
class dgUIAlert(dgUIChoose):
    def __init__(self, scrn, msg,appname="ALERT"):
        dgUIChoose.__init__(self, scrn, msg,["OK"],appname)





#
# class dgUIList
#
class dgUIList(dgUI):
    def __init__(self, scrn, list, pos = 0, appname = "LIST", cursor = True, shadow = True):
        self.name = appname
    
        dgUI.__init__(self, scrn, appname)

        self.shadow = shadow

        # calculates height of the font

        wh = get_string_size("ABCDEFG")
        
        self.disp_last = 0
        self.disp_line_h = wh[1]
        self.disp_lines = (self.sh - self.title_h) / self.disp_line_h

        self.cursor_mode = cursor
        
        self.set_list(list, pos)
        
        self.result = CANCEL
        

    def set_list(self, list, pos = 0):
    
        self.list = list
        self.listlen = len(list)
        self.set_pos(pos)
        
        self.dispbuf = []
        for i in range(self.disp_lines):
            self.dispbuf.append(None)
            
        self.buf = range(self.disp_lines)
        self.bufpos = 0 - self.disp_lines
        self.bottom_line = 0
        self.bottom_step = 0
        
        self.top_steps = 0
        
        self.render_current()


    def set_pos(self, pos):

        # scroll position        
        max = self.listlen - 1
        if max < 0:
            max = 0

        self.pos = dgCount(pos = pos, max = max, loop = False)

        # cursor limit
        max = self.disp_lines - 1
                
        if self.listlen - 1 < max:
            max = self.listlen - 1

        self.cursor = dgCount(pos = 0, max = max, loop = False)

        self.top_step = 0


    def keydown(self, e):
        self.update = True

        if e.key == SELECT or e.key == B:
            return True

        if e.key == UP:
            self.scroll_prev()

        if e.key == DOWN:
            self.scroll_next()
        
        if e.key == START:
            self.result = self.pos.pos + self.cursor.pos
            return True


    def scroll_prev(self):
        if self.cursor_mode:
            if not self.cursor.dec():
                self.render_current()
                return
        
        # check top of the text
        
        if self.top_step > 0:
            self.top_step -= 1
        else:
            self.top_step = -1
            self.pos.dec()

        self.render_current()
        
    def scroll_next(self):
    
        if self.cursor_mode:
            if not self.cursor.inc():
                self.render_current()
                return

        # check bottom of the text
        
        if self.cursor_mode:
            if self.bottom_line < self.listlen:
                self.pos.inc()
                self.render_current()

            return
        
        # return if last line is exposed
        
        if self.bottom_line == self.listlen:
            if self.bottom_step + 1 >= self.bottom_steps:
                return
       
        
        if self.top_step + 1 < self.top_steps:
            self.top_step += 1
        else:
            self.top_step = 0
            self.pos.inc()
            
        self.render_current()
    

    def render_current(self):
    
        c    = self.conf["color"]["textcolor"]
        cs   = self.conf["color"]["shadow"]
        csel = self.conf["color"]["select"]
        
        dl = self.disp_lines
        l = self.listlen
        i = 0
        j = 0
        
        l_empty = self.render_string_lines(" ", c, cs, shadow=self.shadow)
        
        newbuf = []
        top_steps = -1
        skip_lines = self.top_step
                
        while j < dl:
        
            if self.pos.pos + i < l:
                line = self.list[ i + self.pos.pos ]
                line = re.sub ( "\t","    ", line )
                
                # if cursor mode
                if self.cursor_mode and i == self.cursor.pos:
                
                    l_lines = self.render_string_lines(
                        line, csel, cs, shadow=self.shadow)
                    
                    newbuf.append( None )
                
                # normal mode
                else:
                    pos = ( i + self.pos.pos ) - self.bufpos
                    l_lines = self.read_buf( pos )
                    
                    if l_lines is None:
                        l_lines = self.render_string_lines(
                            line, c, cs, shadow=self.shadow)
                                            
                    newbuf.append(l_lines)
                
                # next line
                i += 1
            
            else:
                l_lines = l_empty
            
            if top_steps < 0:
                top_steps = len(l_lines)
                
                # previous line
                if skip_lines < 0:
                    skip_lines = top_steps - 1
                    self.top_step = skip_lines
            
            # fill the buffer
            for k in range ( len(l_lines) ):
                if skip_lines > 0:
                    skip_lines -= 1
                    continue

                self.dispbuf[ j ] = l_lines[ k ]
                j += 1
                if j >= dl:
                    break
    
        self.top_steps = top_steps
        self.bottom_line = self.pos.pos + i
        self.bottom_steps = len( l_lines )
        self.bottom_step = k
        
        self.bufpos = self.pos.pos
        self.buf = newbuf
       
    
    
    def read_buf(self, i):
        if i < 0 or i >= len( self.buf ):
            return None
        
        return self.buf[i]

    
    def draw(self):
        sw = self.sw
        sh = self.sh

        self.base_screen()

        x = 0
        y = 10
        
        for i in range(self.disp_lines):
        
            line = self.dispbuf[i]
        
            if line is not None:

                self.scrn.blit(line, (x,y))
            
            y += line.get_height()

                        
#
# class for test routines
#

class dgUITest(dgUI):
    def draw(self):
        sw = self.sw
        sh = self.sh
        
        c = self.conf["color"]["textcolor"]
        cs = self.conf["color"]["shadow"]
        
        self.base_screen()
        self.draw_string(
            "WELCOME TO DGTK!!", sw / 2, sh / 2,
            c, cs, True, shadow = self.shadow)

        self.draw_string(
            "LARGE!!", sw / 2, sh - (sh / 4),
            c, cs, True, name="l", shadow=self.shadow)

class dgUITestDraw(dgUI):
    def draw(self):
        sw = self.sw
        sh = self.sh
        
        c = self.conf["color"]["textcolor"]
        cs = self.conf["color"]["shadow"]
        
        self.base_screen()

        # draw 4x4 boxes
        
        idx = 0
        
        sx = (sw / 4)
        sy = (sh / 4)
        w = (sw / 4) * 0.7
        h = (sh / 4) * 0.7
        
        bx = (sx - w) / 2
        by = (sy - h) / 2
        y = by
        for j in range(4):
            x = bx
            for i in range(4):
                self.draw_box(x, y, w, h, c, cs, "%d" % idx)
                idx = idx + 1
                x = x + sx

            y = y + sy
    

#
# main for test
#

if __name__=='__main__':
  
    pygame.init()
    pygame.mouse.set_visible(False)

    init( pygame.display.set_mode([320,240]) )

    ui = dgUITest(screen, "DGTK UI TEST ver 1.1")
    ui.loop()
    
    
    ui = dgUITestDraw(screen, "DRAWING BOXES")
    ui.loop()

    size = ["SHORT","TALL","GRANDE","VENTI"]
    
    ui = dgUIChoose(screen, "WHICH SIZE DO YOU LIKE?",size)
    ui.loop()
    
    if ui.result >= 0:
        ui = dgUIAlert(screen, "RESULT = %s" % size[ui.result])
        ui.loop()
    
    
    
    ui = dgUIYesNoChoose(screen, "DO YOU LIKE SUSHI?")
    ui.loop()
    
    ui = dgUIAlert(screen, "RESULT = %d" % ui.result)
    ui.loop()

    ui = dgUIOKChoose(screen, "OK?!")
    ui.loop()
    
    ui = dgUIChoose(screen, "RESULT = %d" % ui.result, ["OK"])
    ui.loop()


    
    list = []
    for i in range(50):
        list.append("%04d : FILE%04d.txt" % ( i , i ) )
    
    ui = dgUIList(screen, list, cursor=False)
    ui.loop()

    ui = dgUIChoose(screen, "INDEX = %d" % ui.result, ["OK"])
    ui.loop()


    

    

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# pyFILER Copyright (C) 2012 by BouKiCHi
#
# This is a subclass of dgTK
#
# The code is provided under the MIT License
#
# Please see the below URL for the detail
# http://opensource.org/licenses/mit-license.php
#

import os
import pygame
import dgtk
import dircache

class dgUIFiler(dgtk.dgUIList):


    def __init__ (self, screen, cwd="/", caption="CHOOSE FILE"):
        self.name = caption
        self.load_dir(cwd)
        dgtk.dgUIList.__init__(self, screen, self.dirlist, appname=caption)
        
        self.set_caption(" %s : [%s]" % (self.name, cwd))
        self.result = None
    
    def load_dir(self, cwd):
        self.cwd = cwd
        
        self.dirlist = [".."] + dircache.listdir(u"%s" % cwd)
        dircache.annotate(cwd, self.dirlist)
        
        self.set_caption(" %s : [%s]" % (self.name, cwd))
    
    def getcwd(self):
        return self.cwd
        
    def keydown ( self , e ):
        self.update = True
        
        if e.key == dgtk.B:
            newpath = os.path.join(self.cwd, "../")
            newpath = os.path.normpath(newpath)
            self.load_dir(newpath)
            self.set_list(self.dirlist)
            return False

        if e.key == dgtk.START or e.key == dgtk.A:
            sel = self.dirlist[self.pos.pos + self.cursor.pos]

            # List is updated if chosen is directory.
            
            if sel[-1] == '/':
                newpath = os.path.join(self.cwd, sel[0:-1])
                newpath = os.path.normpath(newpath)
                self.load_dir(newpath)
                self.set_list(self.dirlist)
            else:
                self.result = os.path.join(self.cwd, sel)
                return True
                
            return False
                
        else:
            return dgtk.dgUIList.keydown(self, e)

#
# main for test
#
if __name__=='__main__':
    fontfile = "DroidSansFallback.ttf"

    pygame.init()
    pygame.mouse.set_visible(False)
    
    screen = pygame.display.set_mode([320, 240])

    dgtk.init(screen)
    dgtk.load_font("m", fontfile, 12)

    ui = dgUIFiler(screen, os.getcwd(), "pyFILER 1.0")
    ui.loop()

    print "result = %s" % ui.result
    



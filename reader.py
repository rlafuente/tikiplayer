#!/usr/bin/env python

import os
import pytiki as ti

'''
Caveats:
    * the returned values are totally unpredictable if two or more tags
      are read simultaneously
    * the script has to be run as root, nothing we can do here as libusb
      requires it
'''

class TikiReader:
    def __init__(self):
        ti.tiki_init()
        ti.tiki_config(5000,0)
        self.tag = None
        self.isPlayerRunning = False

    def read(self):
        num = ti.tiki_seek()
        if num == 0:
            pass
        elif num == 1:
           	idstring = self.parse_id('%x' % ti.tiki_getID1())
           	self.go_amarok(idstring.lower())
        elif num == 2:
            self.parse_id2('%x' % ti.tiki_getID1(), '%x' % ti.tiki_getID2())
        else:
            print "Nope"

    def go_amarok(self, idstring):
       	if self.tag != idstring.lower():
       	    if not self.isPlayerRunning:
       	        os.system('amarok')
       	        self.isPlayerRunning = True
       	    self.tag = idstring.lower()
            os.system('amarok --enqueue %s.mp3' % self.tag)
            os.system('amarok --stop')
            from time import sleep
            sleep(3)
            os.system('amarok --next')
            os.system('amarok --play')

    def go_mplayer(self, idstring):
       	if self.tag != idstring.lower():
       	    self.tag = idstring.lower()
            os.system('pkill mplayer')
            os.spawnv('mplayer %s.mp3' % self.tag)
            
        #os.popen('pkill mplayer')
        #os.popen('mplayer %s.mp3' % idstring)

    def close(self):    
        ti.tiki_close()

    def parse_id(self, id1):
        # sometimes the id starts with 'ffffffff', let's take that out
        if id1.startswith('f'*8):
            id1 = id1[8:17]
        return id1

    def parse_id2(self, id1, id2):
        # don't know what this is for, but Michael put it here so i keep it
        return id1, id2

# do the magic!
t = TikiReader()
try:
    while 1:
        t.read()

except KeyboardInterrupt:
    # quit silently on Ctrl-C
    pass

finally:
    # make sure we close the reader, otherwise it would stay open and
    # we'd have to unplug and plug it again
    print 'Closing reader...'
    t.close()

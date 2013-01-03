import sys, os

os.system('pkill mplayer')
os.system('mplayer %s' % sys.argv[1])



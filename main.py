import sys, os
import shell as s
import pg8000 as pg
from utils import print_sys
from exec import execute

if __name__ == '__main__':
    # enable coloured printing
    os.system('')
    # resize window
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=128))
    # instatiante shell and run
    sh = s.Shell('localhost', 'postgres', 'postgres', 'ouroboros', 5432)
    print_sys("Welcome to Ouroboros. Type '@help' for instructions")
    while not sh.exit:
        execute(sh)

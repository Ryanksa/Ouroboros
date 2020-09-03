import sys, os
import shell as s
import pg8000 as pg

if __name__ == '__main__':
    # enable coloured printing
    os.system('')
    # resize window
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=128))
    # instatiante shell and execute
    sh = s.Shell('localhost', 'postgres', 'postgres', 'ouroboros', 5432)
    while not sh.exit:
        user_in = sh.read_input()
        sh.execute(user_in)

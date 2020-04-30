import sys, os
import shell as s
import pg8000 as pg

# TODO: on startup, create ouroboros db if DNE and adjust it according
if __name__ == '__main__':
    # enable coloured printing
    os.system('')
    # resize window
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=128))
    # instatiante shell and execute
    shellInstance = s.shell('localhost', 'postgres', 'postgres', 'ouroboros', 5432)
    while not shellInstance.exit:
        user_in = shellInstance.read_input()
        shellInstance.execute(user_in)

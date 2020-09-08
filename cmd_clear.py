from utils import print_sys
import os

def clear(sh):
    sh.cmd["curr"](sh)
    print_sys("Are you sure you wish to clear the current note's content?")
    confirm = input("(y/n)")
    os.system('cls')
    if confirm.lower() == "y" or confirm.lower() == "yes":
        sh.curr = ""
    else:
        sh.cmd["curr"](sh)
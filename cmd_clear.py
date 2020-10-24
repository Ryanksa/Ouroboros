from utils import print_sys
import exec

def clear(sh):
    exec.cmd["curr"](sh)
    print_sys("Are you sure you wish to clear the current note's content?")
    while (True):
        confirm = input("(y/n)")
        if confirm.lower() == "y" or confirm.lower() == "yes":
            sh.curr = ""
            exec.cmd["curr"](sh)
            break
        elif confirm.lower() == "n" or confirm.lower() == "no":
            exec.cmd["curr"](sh)
            break

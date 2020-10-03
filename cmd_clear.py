from utils import print_sys

def clear(sh):
    sh.cmd["curr"](sh)
    print_sys("Are you sure you wish to clear the current note's content?")
    while (True):
        confirm = input("(y/n)")
        if confirm.lower() == "y" or confirm.lower() == "yes":
            sh.curr = ""
            sh.cmd["curr"](sh)
            break
        elif confirm.lower() == "n" or confirm.lower() == "no":
            sh.cmd["curr"](sh)
            break

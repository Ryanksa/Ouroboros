from utils import print_sys
import os

def exit_shell(sh):
    """
    Command @exit: exits Ouroboros
    """
    if sh.curr != "":
        print_sys("There are unsaved changes made to the current note, do you still wish exit?")
        while (True):
            confirm = input("(y/n)")
            if confirm.lower() == "y" or confirm.lower() == "yes":
                sh.cursor.close()
                sh.connection.close()
                sh.exit = True
                break
            elif confirm.lower() == "n" or confirm.lower() == "no":
                os.system('cls')
                break
    else:
        sh.cursor.close()
        sh.connection.close()
        sh.exit = True

from utils import print_sys

def exit_shell(sh):
    """
    Command @exit: exits Ouroboros
    """
    confirm = "y"
    if sh.curr != "":
        print_sys("There are unsaved changes made to the current note, do you still wish exit? (y/n)")
        confirm = input()
    if confirm.lower() == "y" or confirm.lower() == "yes":
        sh.cursor.close()
        sh.connection.close()
        sh.exit = True
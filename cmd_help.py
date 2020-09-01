import webbrowser, os

def help(sh):
    """
    Command @help: Opens the help page of Ouroboros
    """
    webbrowser.open("file://" + os.path.realpath("help\\help.html"), new=2)

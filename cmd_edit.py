import os, sys
from PyQt5.QtWidgets import QApplication
from editor import Editor
import exec

def edit_note(sh, parameters=[]):
    """
    Command @edit:
    set console to edit mode to edit the given or current (if no note was given) note
    """
    if len(parameters) > 1:
        sh.err.raiseInvalidArg("Cannot open more than 1 note at once to edit")
        return None
    elif len(parameters) == 1 and sh.opened != "":
        if sh.opened == parameters[0]:
            parameters = []
        else:
            sh.err.raiseInvalidArg("There is already an opened note. Save and close that one first")
            return None
    
    # open the specified note first
    if len(parameters) == 1:
        exec.cmd["open"](sh, parameters)
    # create a temp file to write curr to
    note = "temp"
    with open(note, 'w+t') as f:
        f.write(sh.curr)
    # open the temp file with custom editor to edit
    app = QApplication(sys.argv)
    editor = Editor(note)
    app.exec_()
    # read out the new curr and remove temp file
    with open(note, 'r') as f:
        new_curr = f.read()
    os.remove(note)
    # update curr
    if new_curr.endswith("\n"):
        sh.curr = new_curr
    else:
        sh.curr = new_curr + "\n"
    exec.cmd["curr"](sh)

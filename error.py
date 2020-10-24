from utils import print_err

class Error:
    def __init__(self):
        pass

    def raiseInvalidCmd(self, errMsg):
        print_err("Not a valid command: " + errMsg)

    def raiseGroupingSyntax(self, synErr):
        print_err("Invalid grouping syntax, expecting: ["+synErr+"}")

    def raiseDNE(self, item):
        if item.startswith('[') and item.endswith('}'):
            print_err("Grouping does not exist: " + item)
        else:
            print_err("Note does not exist: " + item)
    
    def raiseInvalidArg(self, msg):
        print_err("Invalid arguments: " + msg)

    def raiseAlreadyExists(self, note):
        print_err("Note already exists: " + note)

    def raiseAlreadyEditing(self, note):
        print_err("Already editing note: " + note)

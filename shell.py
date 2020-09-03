import os
import pg8000 as pg
from error import Error
from utils import print_sys, print_curr
import cmd_curr, cmd_drop, cmd_edit, cmd_exit, cmd_help, cmd_list, cmd_open, cmd_peek, cmd_query, cmd_rename, cmd_save, cmd_setgrp

class Shell:
    def __init__(self, dbHost, dbUser, dbPassword, dbName, port):
        # DB variables
        self.connection = pg.connect(host=dbHost, user=dbUser, password=dbPassword, database=dbName, port=port)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notes(name VARCHAR(128) NOT NULL, content text, grouping VARCHAR(128))""")
        # error handler
        self.err = Error()
        # other variables
        self.curr = ""
        self.opened = ""
        self.exit = False
        # command variables
        self.cmd = dict()
        self.cmd['help'] = cmd_help.help
        self.cmd['exit'] = cmd_exit.exit_shell
        self.cmd['curr'] = cmd_curr.get_curr
        self.cmd['list'] = cmd_list.list_notes
        self.cmd['drop'] = cmd_drop.drop_notes
        self.cmd['save'] = cmd_save.save_to_notes
        self.cmd['setgrp'] = cmd_setgrp.set_grouping
        self.cmd['rename'] = cmd_rename.rename_note
        self.cmd['open'] = cmd_open.open_note
        self.cmd['edit'] = cmd_edit.edit_note
        self.cmd['query'] = cmd_query.query_notes
        self.cmd['peek'] = cmd_peek.peek_notes
        print_sys("Welcome to Ouroboros. Type '@help' for instructions")

    def read_input(self):
        print("\\" + self.opened + ">", end=" ")
        return input()

    def execute(self, userin):
        """
        parses the user input and either execute a command or store to current note
        """
        if userin.startswith('@'):
            # parse and execute command
            os.system('cls')
            print(userin)
            cmdin = userin.split()
            cmdin[0] = cmdin[0][1:]
            try:
                if len(cmdin) == 1:
                    self.cmd[cmdin[0]](self)
                else:
                    self.cmd[cmdin[0]](self, cmdin[1:])
            except:
                self.err.raiseInvalidCmd()
        else:
            # store to current note
            self.curr += userin + "\n"
            os.system('cls')
            print_curr(self.curr)

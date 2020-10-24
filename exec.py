import os
from utils import print_curr
import cmd_clear, cmd_curr, cmd_drop, cmd_edit, cmd_exit, cmd_help, cmd_list, cmd_open, cmd_peek, cmd_query, cmd_rename, cmd_save, cmd_setgrp

cmd = dict()
cmd['help'] = cmd_help.help
cmd['exit'] = cmd_exit.exit_shell
cmd['curr'] = cmd_curr.get_curr
cmd['clear'] = cmd_clear.clear
cmd['list'] = cmd_list.list_notes
cmd['drop'] = cmd_drop.drop_notes
cmd['save'] = cmd_save.save_to_notes
cmd['setgrp'] = cmd_setgrp.set_grouping
cmd['rename'] = cmd_rename.rename_note
cmd['open'] = cmd_open.open_note
cmd['edit'] = cmd_edit.edit_note
cmd['query'] = cmd_query.query_notes
cmd['peek'] = cmd_peek.peek_notes

def execute(sh):
    """
    reads and parses the user input to either execute a command or store to current note
    """
    print("\\" + sh.opened + ">", end=" ")
    userin = input()
    if userin.startswith('@'):
        # parse and execute command
        os.system('cls')
        print(userin)
        cmdin = userin.split()
        cmdin[0] = cmdin[0][1:]
        try:
            if len(cmdin) == 1:
                cmd[cmdin[0]](sh)
            else:
                cmd[cmdin[0]](sh, cmdin[1:])
        except Exception as e:
            sh.err.raiseInvalidCmd(str(e))
    else:
        # store to current note
        sh.curr += userin + "\n"
        os.system('cls')
        print_curr(sh.curr)

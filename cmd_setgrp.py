import exec

def set_grouping(sh, parameters=None):
    """
    Command @setgrp:
    given a grouping and a list of notes, set those notes to be of the specified grouping
    """
    # no arguments given
    if parameters is None:
        sh.err.raiseInvalidArg("Please specify the note and grouping to set it to")
    # only 1 argument given
    elif len(parameters) == 1:
        sh.raiseInvalidArg("There should be at least 2 arguments")
    else:
        grouping = parameters[0]
        # the first given argument is not the grouping, raise error
        if grouping.startswith("[") and grouping.endswith("}"):
            grouping = grouping[1:-1]
        else:
            sh.err.raiseGroupingSyntax(grouping)
            return None
        # loop thru the rest of the arguments to set groupings
        list_of_notes = parameters[1:]
        # case of setting empty grouping
        if grouping == "":
            for note in list_of_notes:
                sh.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                if sh.cursor.fetchone() is not None:
                    sh.cursor.execute("""UPDATE notes SET grouping = NULL WHERE name = %s""", (note,))
                else:
                    sh.err.raiseDNE(note)
        # case of setting non-empty grouping
        else:
            for note in list_of_notes:
                sh.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                if sh.cursor.fetchone() is not None:
                    sh.cursor.execute("""UPDATE notes SET grouping = %s WHERE name = %s""", (grouping, note,))
                else:
                    sh.err.raiseDNE(note)        
    sh.connection.commit()
    exec.cmd["list"](sh)

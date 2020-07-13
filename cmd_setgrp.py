def set_grouping(sh, parameters=None):
    """
    Command @setgrp:
    given a grouping and a list of notes, set those notes to be of the specified grouping
    """
    if parameters is None:
        sh.err.raiseInvalidArg("Please specify the note and grouping to set it to")
    elif len(parameters) >= 2:
        grouping = parameters[0]
        if grouping.startswith("[") and grouping.endswith("}"):
            grouping = grouping[1:-1]
        else:
            sh.err.raiseGroupingSyntax(grouping)
            return None
        list_of_notes = parameters[1:]
        if grouping == "":
            for note in list_of_notes:
                sh.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                if sh.cursor.fetchone() is not None:
                    sh.cursor.execute("""UPDATE notes SET grouping = NULL WHERE name = %s""", (note,))
                else:
                    sh.err.raiseDNE(note)
        else:
            for note in list_of_notes:
                sh.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                if sh.cursor.fetchone() is not None:
                    sh.cursor.execute("""UPDATE notes SET grouping = %s WHERE name = %s""", (grouping, note,))
                else:
                    sh.err.raiseDNE(note)
    else:
        sh.raiseInvalidArg("There should be at least 2 arguments")
    sh.connection.commit()
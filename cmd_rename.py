def rename_note(sh, parameters=None):
    """
    Command @rename:
    given the original name and the new name of a note, rename the note
    """
    if parameters is None:
        sh.err.raiseInvalidArg("Please specify the note to rename")
    elif len(parameters) == 2:
        old_name = parameters[0]
        new_name = parameters[1]
        sh.cursor.execute("""SELECT name FROM notes WHERE name = %s""", (old_name,))
        old = sh.cursor.fetchone()
        sh.cursor.execute("""SELECT name FROM notes WHERE name = %s""", (new_name,))
        new = sh.cursor.fetchone()
        if old is None:
            sh.err.raiseDNE(oldname)
            return None
        elif new is not None:
            sh.err.raiseAlreadyExists(new_name)
            return None
        else:
            sh.cursor.execute("""UPDATE notes SET name = %s WHERE name = %s""", (new_name, old_name,))
        # update opened if applicable
        if old_name == sh.opened:
            sh.opened = new_name
    else:
        sh.raiseInvalidArg("Exactly 2 arguments should be used")
    sh.connection.commit()
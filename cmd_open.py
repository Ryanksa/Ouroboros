def open_note(sh, parameters=None):
    """
    open the given note to curr, keeping track of the opened note
    """
    # no specified note to open
    if parameters is None:
        sh.err.raiseInvalidArg("Please specify the note to open")
        return None
    # too many arguments or there is already an opened note
    elif len(parameters) > 1 or (sh.opened != "" and sh.opened != parameters[0]):
        sh.err.raiseInvalidArg("Cannot open more than 1 note at once")
        return None
    note = parameters[0]
    # specified note is already open
    if note == sh.opened:
        sh.err.raiseInvalidArg("Specified note is already open")
        return None
    # tried to open a grouping of notes
    elif note.startswith("[") and note.endswith("}"):
        sh.err.raiseInvalidArg("Cannot open a grouping of notes")
        return None
    
    # open the specified note
    sh.cursor.execute("""SELECT content FROM notes WHERE name = %s""", (note,))
    content = sh.cursor.fetchone()
    if content is None:
        sh.err.raiseDNE(note)
        return None
    sh.opened = note
    sh.curr = content[0]
    sh.cmd["curr"](sh)

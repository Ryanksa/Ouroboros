def save_to_notes(sh, list_of_items=[]):
    """
    Command @save:
    given a list of items, note and/or grouping, save the current note to those notes and groupings of notes
    """
    # if there is an opened note, save to it as well
    if sh.opened != "":
        list_of_items.append(sh.opened)
    
    # throw error if no item given
    if len(list_of_items) == 0:
        sh.err.raiseInvalidArg("Please specify notes or grouping to save to")
        return None

    # look thru all the grouping items first, adding the notes under them to saveto_notes
    saveto_notes = set()
    groupings = [item[1:-1] for item in list_of_items if item.startswith("[") and item.endswith("}")]
    for group in groupings:
        # get the notes under this grouping
        if group == "":
            sh.cursor.execute("""SELECT name FROM notes WHERE grouping IS NULL""")
        else:
            sh.cursor.execute("""SELECT name FROM notes WHERE grouping = %s""", (group,))
        saveto_note = sh.cursor.fetchone()
        # no notes under this grouping (grouping DNE), throw error and continue
        if saveto_note is None:
            sh.err.raiseDNE("[" + group + "}")
            continue
        # add notes under this grouping to saveto_notes
        while saveto_note is not None:
            saveto_notes.add(saveto_note[0])
            saveto_note = sh.cursor.fetchone()

    # get all individual notes
    origSet = {item for item in list_of_items if not item.startswith("[") or not item.endswith("}")}
    newSet = saveto_notes.union(origSet)
    # for each note, (create first if DNE) save to it
    for note in newSet:
        sh.cursor.execute("""SELECT content FROM notes WHERE name = %s""", (note,))
        note_content = sh.cursor.fetchone()
        if note_content is None:
            # not an existing note, create and save content
            sh.cursor.execute("""INSERT INTO notes(name, content) VALUES(%s, %s)""", (note, sh.curr,))
        else:
            # existing note, check if it was opened, then save to it
            if note == sh.opened:
                new_content_str = sh.curr
                sh.opened = ""
            else:
                new_content_str = note_content[0] + sh.curr
            sh.cursor.execute("""UPDATE notes SET content = %s WHERE name = %s""", (new_content_str, note,))
    sh.connection.commit()
    sh.curr = ""
def save_to_notes(sh, list_of_items=[]):
    """
    Command @save:
    given a list of items, note and/or grouping, save the current note to those notes and groupings of notes
    """
    # throw error if no item given
    if len(list_of_items) == 0 and sh.opened == "":
        sh.err.raiseInvalidArg("Please specify notes or grouping to save to")
        return None
    
    # look thru all the grouping first, adding the notes under them into a set
    groupingItems = set()
    groupingsList = [item[1:-1] for item in list_of_items if item.startswith("[") and item.endswith("}")]
    for grouping in groupingsList:
        # get the notes under this grouping
        if grouping == "":
            sh.cursor.execute("""SELECT name FROM notes WHERE grouping IS NULL""")
        else:
            sh.cursor.execute("""SELECT name FROM notes WHERE grouping = %s""", (grouping,))
        note = sh.cursor.fetchone()
        # no notes under this grouping, throw error and continue
        if note is None:
            sh.err.raiseDNE("[" + grouping + "}")
            continue
        # add notes under this grouping to the set
        while note is not None:
            groupingItems.add(note[0])
            note = sh.cursor.fetchone()

    # union all grouping items with note items into one set
    noteItems = {item for item in list_of_items if not item.startswith("[") or not item.endswith("}")}
    allItems = groupingItems.union(noteItems)
    # if there is an opened note, add it to the set
    if sh.opened != "":
        allItems.add(sh.opened)
    
    # for each note in the set, save to it
    for note in allItems:
        sh.cursor.execute("""SELECT content FROM notes WHERE name = %s""", (note,))
        note_content = sh.cursor.fetchone()
        # not an existing note, create and save content
        if note_content is None:
            sh.cursor.execute("""INSERT INTO notes(name, content) VALUES(%s, %s)""", (note, sh.curr,))
        # existing note, check if it was opened, then save to it
        else:
            if note == sh.opened:
                new_content = sh.curr
            else:
                new_content = note_content[0] + sh.curr
            sh.cursor.execute("""UPDATE notes SET content = %s WHERE name = %s""", (new_content, note,))

    sh.connection.commit()
    sh.curr = ""
    sh.opened = ""
    sh.cmd["list"](sh)

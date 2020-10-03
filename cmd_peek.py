import re
from utils import print_sys, build_title

def peek_notes(sh, list_of_items=[]):
    """
    Command @peek:
    given a list of items, note and/or grouping, peek the notes and groupings of notes
    """
    # no argument given, raise error
    if len(list_of_items) == 0:
        sh.err.raiseInvalidArg("Please specify notes and/or groupings of notes")
        return None

    for item in list_of_items:
        # item is a grouping of notes
        if item.startswith("[") and item.endswith("}"):
            group = item[1:-1]
            if group == "":
                sh.cursor.execute("""SELECT name FROM notes WHERE grouping IS NULL ORDER BY name""")
            else:
                sh.cursor.execute("""SELECT name FROM notes WHERE grouping = %s ORDER BY name""", (group,))
            peek_note = sh.cursor.fetchone()
            if peek_note is None:
                sh.err.raiseDNE("[" + group + "}")
                continue
            list_of_peek_notes = []
            while peek_note is not None:
                list_of_peek_notes.append(peek_note[0])
                peek_note = sh.cursor.fetchone()
            peek_notes(sh, list_of_peek_notes)
        # item is a note
        else:
            sh.cursor.execute("""SELECT content, grouping FROM notes WHERE name = %s""", (item,))
            content_grouping = sh.cursor.fetchone()
            if content_grouping is not None:
                if content_grouping[1] is None:
                    content_grouping[1] = ""
                noteTitle = build_title(content_grouping[1], item)
                print_sys(noteTitle + "\n" + content_grouping[0][:-1])
            else:
                sh.err.raiseDNE(item)

from utils import print_sys

def list_notes(sh, groupings=[]):
    """
    Command @list:
    if no grouping is given, list all the existing notes
    if groupings are given, list all the existing notes under those groupings
    """
    if len(groupings) == 0:
        # no grouping given, list all notes
        sh.cursor.execute("""SELECT name, grouping FROM notes ORDER BY grouping, name""")
        list_of_notes = sh.cursor.fetchall()
        output = ""
        for note_tuple in list_of_notes:
            if note_tuple[1] is None:
                note_tuple[1] = ""
            output += "[" + note_tuple[1] + "} " + note_tuple[0] + "\n"
        print_sys(output[:-1])
    else:
        # groupings given, list notes under those groupings
        output = ""
        for grouping in groupings:
            if grouping.startswith("[") and grouping.endswith("}"):
                grouping = grouping[1:-1]
                if grouping == "":
                    sh.cursor.execute("""SELECT name, grouping FROM notes WHERE grouping IS NULL ORDER BY name""")
                else:
                    sh.cursor.execute("""SELECT name, grouping FROM notes WHERE grouping = %s ORDER BY name""", (grouping,))
                list_of_notes = sh.cursor.fetchall()
                for note_tuple in list_of_notes:
                    if note_tuple[1] is None:
                        note_tuple[1] = ""
                    output += "[" + note_tuple[1] + "} " + note_tuple[0] + "\n"
            else:
                sh.err.raiseGroupingSyntax(grouping)
        print_sys(output[:-1])

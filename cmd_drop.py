from utils import print_sys

def drop_notes(sh, list_of_items=[]):
    """
    Command @drop:
    if no list is given, deletes all existing notes
    if a list of items, note and/or grouping, is given, delete those notes and groupings of notes
    """
    if len(list_of_items) == 0:
        # no item given, delete all notes
        print_sys("Are you sure you wish to delete ALL saved notes? (y/n)")
        confirm = input()
        if confirm.lower() == "y" or confirm.lower() == "yes":
            sh.cursor.execute("""DROP TABLE notes""")
            sh.cursor.execute("""CREATE TABLE notes(name VARCHAR(128) NOT NULL, content text, grouping VARCHAR(128))""")
    else:
        # items given, delete given items
        for item in list_of_items:
            if item.startswith("[") and item.endswith("}"):
                group = item[1:-1]
                if group == "":
                    sh.cursor.execute("""SELECT * FROM notes WHERE grouping IS NULL""")
                    if sh.cursor.fetchone() is not None:
                        sh.cursor.execute("""DELETE FROM notes WHERE grouping IS NULL""")
                    else:
                        sh.err.raiseDNE("[}")
                else:
                    sh.cursor.execute("""SELECT * FROM notes WHERE grouping = %s""", (group,))
                    if sh.cursor.fetchone() is not None:
                        sh.cursor.execute("""DELETE FROM notes WHERE grouping = %s""", (group,))
                    else:
                        sh.err.raiseDNE("[" + group + "}")
            
            else:
                sh.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (item,))
                if sh.cursor.fetchone() is not None:
                    sh.cursor.execute("""DELETE FROM notes WHERE name = %s""", (item,))
                else:
                    sh.err.raiseDNE(item)
    sh.connection.commit()

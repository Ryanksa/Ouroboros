import re
from utils import print_sys, highlighter

def query_notes(sh, parameters=None):
    """
    Command @query:
    queries all existing notes to look for the pattern given in parameters
    if the pattern uses spaces, it must be surronded by single/double quotations
    """
    # no arguments given, raise error
    if parameters is None:
        sh.err.raiseInvalidArg("Missing the pattern to query for.")
    grouping = None
    pattern = ""
    # check if there is a specified grouping to search in
    if parameters[0].startswith("[") and parameters[0].endswith("}"):
        grouping = parameters[0][1:-1]
        parameters = parameters[1:]
    # parse the pattern
    if (parameters[0].startswith('"') and parameters[-1].endswith('"')) or (
            parameters[0].startswith("'") and parameters[-1].endswith("'")):
        parameters[0] = parameters[0][1:]
        parameters[-1] = parameters[-1][:-1]
        for word in parameters:
            pattern += " " + word
        pattern = "%" + pattern[1:] + "%"
        regex = pattern[1:-1]
    elif len(parameters) > 1:
        sh.err.raiseInvalidArg("Can only query for 1 pattern at a time.")
    else:
        pattern = "%" + parameters[0] + "%"
        regex = parameters[0]
    # search for the given pattern
    if grouping is None:
        sh.cursor.execute("""SELECT * FROM notes WHERE name ILIKE %s OR content ILIKE %s ORDER BY grouping DESC"""
                            , (pattern, pattern,))
    elif grouping == "":
        sh.cursor.execute("""SELECT * FROM notes WHERE grouping IS NULL AND (name ILIKE %s OR content ILIKE %s)"""
                            , (pattern, pattern,))
    else:
        sh.cursor.execute("""SELECT * FROM notes WHERE grouping = %s AND (name ILIKE %s OR content ILIKE %s)"""
                            , (grouping, pattern, pattern,))
    list_of_notes = sh.cursor.fetchall()
    # display the search results
    for note_tuple in list_of_notes:
        if note_tuple[2] is None:
            note_tuple[2] = ""
        noteName = "[" + note_tuple[2] + "} " + note_tuple[0]
        colored_content = re.sub(regex, highlighter, note_tuple[1][:-1], flags=re.I)
        print_sys(" "*(128-len(noteName)) + noteName + "\n" + colored_content)

import os, sys, re
import pg8000 as pg
from PyQt5.QtWidgets import QApplication
from editor import Editor
from error import Error

# TODO: improve code efficiency and readability
class shell:
    def __init__(self, dbHost, dbUser, dbPassword, dbName, port):
        # DB variables
        self.connection = pg.connect(host=dbHost, user=dbUser, password=dbPassword, database=dbName, port=port)
        self.cursor = self.connection.cursor()
        # error handler
        self.err = Error()
        # other variables
        self.curr = ""
        self.opened = ""
        self.exit = False
        # command variables
        self.cmd = dict()
        self.cmd['help'] = self.help
        self.cmd['exit'] = self.exit_shell
        self.cmd['curr'] = self.get_curr
        self.cmd['list'] = self.list_notes
        self.cmd['drop'] = self.drop_notes
        self.cmd['save'] = self.save_to_notes
        self.cmd['setgrp'] = self.set_grouping
        self.cmd['rename'] = self.rename_note
        self.cmd['open'] = self.open_note
        self.cmd['edit'] = self.edit_note
        self.cmd['query'] = self.query_notes
        self.cmd['peek'] = self.peek_notes
        print_sys("Welcome to Ouroboros. Type '@help' for instructions")

    def read_input(self):
        print("\n\\" + self.opened + ">", end=" ")
        return input()

    def execute(self, userin):
        """
        parses the user input and either execute a command or store to current note
        """
        if userin.startswith('@'):
            # parse and execute command
            os.system('cls')
            print(userin)
            cmdin = userin.split()
            cmdin[0] = cmdin[0][1:]
            try:
                if len(cmdin) == 1:
                    self.cmd[cmdin[0]]()
                else:
                    self.cmd[cmdin[0]](cmdin[1:])
            except:
                self.err.raiseInvalidCmd()
        else:
            # store to current note
            self.curr += userin + "\n"
            os.system('cls')
            print_curr(self.curr)

    def help(self):
        """
        prints out instructions on how to use Ouroboros
        """
        # TODO: improve @help to be more intuitive
        instructions = "Ouroboros is a writing tool. Type to start writing, or perform a command with @\n\
@exit: exit this shell\n\
@curr: switch console over to the current note\n\
@list [groupingName}: list all notes, under a certain grouping name if included\n\
@drop noteName [groupingName}: remove notes and grouping of notes as specified. If nothing is specified remove all notes\n\
@save noteName [groupingName}: save the current note into the specified notes and grouping of notes\n\
@setgrp [groupingName} noteName: set the grouping for the specified notes\n\
@rename oldNoteName newNoteName: rename oldNoteName to newNoteName\n\
@open noteName: opens the specified note to curr, saving back to the opened note will replace the content\n\
@edit noteName: edit the given or current (if none was given) note in edit mode\n\
@query [groupingName} 'pattern': queries and open all notes, under grouping if specified, with the given pattern\n\
@peek noteName [groupingName}: peek at the specified notes and groupings of notes"
        print_sys(instructions)

    def exit_shell(self):
        """
        exits Ouroboros
        """
        self.cursor.close()
        self.connection.close()
        self.exit = True

    def get_curr(self):
        """
        switch over to the current note
        """
        os.system('cls')
        print_curr(self.curr)
        
    def list_notes(self, groupings=[]):
        """
        if no grouping is given, list all the existing notes
        if groupings are given, list all the existing notes under those groupings
        """
        if len(groupings) == 0:
            # no grouping given, list all notes
            self.cursor.execute("""SELECT name, grouping FROM notes ORDER BY grouping DESC""")
            list_of_notes = self.cursor.fetchall()
            for note_tuple in list_of_notes:
                if note_tuple[1] is None:
                    note_tuple[1] = ""
                print_sys("[" + note_tuple[1] + "} " + note_tuple[0])
        else:
            # groupings given, list notes under those groupings
            for grouping in groupings:
                if grouping.startswith("[") and grouping.endswith("}"):
                    grouping = grouping[1:-1]
                    if grouping == "":
                        self.cursor.execute("""SELECT name, grouping FROM notes WHERE grouping IS NULL""")
                    else:
                        self.cursor.execute("""SELECT name, grouping FROM notes WHERE grouping = %s""", (grouping,))
                    list_of_notes = self.cursor.fetchall()
                    for note_tuple in list_of_notes:
                        if note_tuple[1] is None:
                            note_tuple[1] = ""
                        print_sys("[" + note_tuple[1] + "} " + note_tuple[0])
                else:
                    self.err.raiseGroupingSyntax(grouping)

    def drop_notes(self,  list_of_items=[]):
        """
        if no list is given, deletes all existing notes
        if a list of items, note and/or grouping, is given, delete those notes and groupings of notes
        """
        if len(list_of_items) == 0:
            # no item given, delete all notes
            self.cursor.execute("""DROP TABLE notes""")
            self.cursor.execute("""CREATE TABLE notes(name VARCHAR(128) NOT NULL, content text, grouping VARCHAR(128))""")
        else:
            # items given, delete given items
            for item in list_of_items:
                if item.startswith("[") and item.endswith("}"):
                    group = item[1:-1]
                    if group == "":
                        self.cursor.execute("""SELECT * FROM notes WHERE grouping IS NULL""")
                        if self.cursor.fetchone() is not None:
                            self.cursor.execute("""DELETE FROM notes WHERE grouping IS NULL""")
                        else:
                            self.err.raiseDNE("[}")
                    else:
                        self.cursor.execute("""SELECT * FROM notes WHERE grouping = %s""", (group,))
                        if self.cursor.fetchone() is not None:
                            self.cursor.execute("""DELETE FROM notes WHERE grouping = %s""", (group,))
                        else:
                            self.err.raiseDNE("[" + group + "}")
                
                else:
                    self.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (item,))
                    if self.cursor.fetchone() is not None:
                        self.cursor.execute("""DELETE FROM notes WHERE name = %s""", (item,))
                    else:
                        self.err.raiseDNE(item)
        self.connection.commit()

    def save_to_notes(self, list_of_items=[]):
        """
        given a list of items, note and/or grouping, save the current note to those notes and groupings of notes
        """
        # if there is an opened note, save to it as well
        if self.opened != "":
            list_of_items.append(self.opened)
        
        # throw error if no item given
        if len(list_of_items) == 0:
            self.err.raiseInvalidArg("Please specify notes or grouping to save to")
            return None

        # look thru all the grouping items first, adding the notes under them to saveto_notes
        saveto_notes = set()
        groupings = [item[1:-1] for item in list_of_items if item.startswith("[") and item.endswith("}")]
        for group in groupings:
            # get the notes under this grouping
            if group == "":
                self.cursor.execute("""SELECT name FROM notes WHERE grouping IS NULL""")
            else:
                self.cursor.execute("""SELECT name FROM notes WHERE grouping = %s""", (group,))
            saveto_note = self.cursor.fetchone()
            # no notes under this grouping (grouping DNE), throw error and continue
            if saveto_note is None:
                self.err.raiseDNE("[" + group + "}")
                continue
            # add notes under this grouping to saveto_notes
            while saveto_note is not None:
                saveto_notes.add(saveto_note[0])
                saveto_note = self.cursor.fetchone()
    
        # get all individual notes
        origSet = {item for item in list_of_items if not item.startswith("[") or not item.endswith("}")}
        newSet = saveto_notes.union(origSet)
        # for each note, (create first if DNE) save to it
        for note in newSet:
            self.cursor.execute("""SELECT content FROM notes WHERE name = %s""", (note,))
            note_content = self.cursor.fetchone()
            if note_content is None:
                # not an existing note, create and save content
                self.cursor.execute("""INSERT INTO notes(name, content) VALUES(%s, %s)""", (note, self.curr,))
            else:
                # existing note, check if it was opened, then save to it
                if note == self.opened:
                    new_content_str = self.curr
                    self.opened = ""
                else:
                    new_content_str = note_content[0] + self.curr
                self.cursor.execute("""UPDATE notes SET content = %s WHERE name = %s""", (new_content_str, note,))
        self.connection.commit()
        self.curr = ""

    def set_grouping(self, parameters=None):
        """
        given a grouping and a list of notes, set those notes to be of the specified grouping
        """
        if parameters is None:
            self.err.raiseInvalidArg("Please specify the note and grouping to set it to")
        elif len(parameters) >= 2:
            grouping = parameters[0]
            if grouping.startswith("[") and grouping.endswith("}"):
                grouping = grouping[1:-1]
            else:
                self.err.raiseGroupingSyntax(grouping)
                return None
            list_of_notes = parameters[1:]
            if grouping == "":
                for note in list_of_notes:
                    self.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                    if self.cursor.fetchone() is not None:
                        self.cursor.execute("""UPDATE notes SET grouping = NULL WHERE name = %s""", (note,))
                    else:
                        self.err.raiseDNE(note)
            else:
                for note in list_of_notes:
                    self.cursor.execute("""SELECT * FROM notes WHERE name = %s""", (note,))
                    if self.cursor.fetchone() is not None:
                        self.cursor.execute("""UPDATE notes SET grouping = %s WHERE name = %s""", (grouping, note,))
                    else:
                        self.err.raiseDNE(note)
        else:
            self.raiseInvalidArg("There should be at least 2 arguments")
        self.connection.commit()

    def rename_note(self, parameters=None):
        """
        given the original name and the new name of a note, rename the note
        """
        if parameters is None:
            self.err.raiseInvalidArg("Please specify the note to rename")
        elif len(parameters) == 2:
            old_name = parameters[0]
            new_name = parameters[1]
            self.cursor.execute("""SELECT name FROM notes WHERE name = %s""", (old_name,))
            old = self.cursor.fetchone()
            self.cursor.execute("""SELECT name FROM notes WHERE name = %s""", (new_name,))
            new = self.cursor.fetchone()
            if old is None:
                self.err.raiseDNE(oldname)
                return None
            elif new is not None:
                self.err.raiseAlreadyExists(new_name)
                return None
            else:
                self.cursor.execute("""UPDATE notes SET name = %s WHERE name = %s""", (new_name, old_name,))
            # update opened if applicable
            if old_name == self.opened:
                self.opened = new_name
        else:
            self.raiseInvalidArg("Exactly 2 arguments should be used")
        self.connection.commit()

    def open_note(self, parameters=None):
        """
        open the given note to curr, keeping track of the opened note
        """
        if parameters is None:
            self.err.raiseInvalidArg("Please specify the note to open")
            return None
        elif (len(parameters) > 1 or self.opened != ""):
            self.err.raiseInvalidArg("Cannot open more than 1 note at once")
            return None
        note = parameters[0]
        if note.startswith("[") and note.endswith("}"):
            self.err.raiseInvalidArg("Cannot open a grouping of notes")
            return None
        self.cursor.execute("""SELECT content FROM notes WHERE name = %s""", (note,))
        content = self.cursor.fetchone()
        if content is None:
            self.err.raiseDNE(note)
            return None
        self.opened = note
        self.curr = content[0]
        self.get_curr()
        
    def edit_note(self, parameters=[]):
        """
        set console to edit mode to edit the given or current (if no note was given) note
        """
        if len(parameters) > 1:
            self.err.raiseInvalidArg("Cannot open more than 1 note at once to edit")
            return None
        elif len(parameters) == 1 and self.opened != "":
            self.err.raiseInvalidArg("There is already an opened note. Save and close that one first")
            return None
        
        # open the specified note first
        if len(parameters) == 1:
            self.open_note(parameters)
        # create a temp file to write curr to
        note = "temp"
        with open(note, 'w+t') as f:
            f.write(self.curr)
        # open the temp file with custom editor to edit
        app = QApplication(sys.argv)
        editor = Editor(note)
        app.exec_()
        # read out the new curr and remove temp file
        with open(note, 'r') as f:
            new_curr = f.read()
        os.remove(note)
        # update curr
        if new_curr.endswith("\n"):
            self.curr = new_curr
        else:
            self.curr = new_curr + "\n"
        self.get_curr()
        
    def query_notes(self, parameters=None):
        """
        queries all existing notes to look for the pattern given in parameters
        if the pattern uses spaces, it must be surronded by single/double quotations
        """
        grouping = None
        if parameters[0].startswith("[") and parameters[0].endswith("}"):
            grouping = parameters[0][1:-1]
            parameters = parameters[1:]
        pattern = ""
        if (parameters[0].startswith('"') and parameters[-1].endswith('"')) or (
                parameters[0].startswith("'") and parameters[-1].endswith("'")):
            parameters[0] = parameters[0][1:]
            parameters[-1] = parameters[-1][:-1]
            for word in parameters:
                pattern += " " + word
            pattern = "%" + pattern[1:] + "%"
            regex = pattern[1:-1]
        else:
            pattern = "%" + parameters[0] + "%"
            regex = parameters[0]
        if grouping is None:
            self.cursor.execute("""SELECT * FROM notes WHERE name ILIKE %s OR content ILIKE %s ORDER BY grouping DESC"""
                                , (pattern, pattern,))
        elif grouping == "":
            self.cursor.execute("""SELECT * FROM notes WHERE grouping IS NULL AND (name ILIKE %s OR content ILIKE %s)"""
                                , (pattern, pattern,))
        else:
            self.cursor.execute("""SELECT * FROM notes WHERE grouping = %s AND (name ILIKE %s OR content ILIKE %s)"""
                                , (grouping, pattern, pattern,))
        list_of_notes = self.cursor.fetchall()
        for note_tuple in list_of_notes:
            if note_tuple[2] is None:
                note_tuple[2] = ""
            print_sys("\n[" + note_tuple[2] + "} " + note_tuple[0])
            print_sys("=" * 128)
            color_content = re.sub(regex, highlighter, note_tuple[1][:-1], flags=re.I)
            print_sys(color_content)
            print_sys("=" * 128)

    def peek_notes(self, list_of_items=[]):
        """
        given a list of items, note and/or grouping, peek the notes and groupings of notes
        """
        if len(list_of_items) == 0:
            self.err.raiseInvalidArg("Please specify notes and/or groupings of notes")
            return None
        for item in list_of_items:
            if item.startswith("[") and item.endswith("}"):
                group = item[1:-1]
                if group == "":
                    self.cursor.execute("""SELECT name FROM notes WHERE grouping IS NULL""")
                else:
                    self.cursor.execute("""SELECT name FROM notes WHERE grouping = %s""", (group,))
                peek_note = self.cursor.fetchone()
                if peek_note is None:
                    self.err.raiseDNE("[" + group + "}")
                    continue
                list_of_peek_notes = []
                while peek_note is not None:
                    list_of_peek_notes.append(peek_note[0])
                    peek_note = self.cursor.fetchone()
                self.peek_notes(list_of_peek_notes)
            else:
                self.cursor.execute("""SELECT content, grouping FROM notes WHERE name = %s""", (item,))
                content_grouping = self.cursor.fetchone()
                if content_grouping is not None:
                    if content_grouping[1] is None:
                        content_grouping[1] = ""
                    print_sys("\n[" + content_grouping[1] + "} " + item)
                    print_sys("=" * 128)
                    print_sys(content_grouping[0][:-1])
                    print_sys("=" * 128)
                else:
                    self.err.raiseDNE(item)


# internal static helpers to print in colors
def print_curr(text):
    prepender = lambda m: '\u001b[32m::\u001b[0m'.format(m.group())
    print_text = re.sub("^", prepender, text[:-1], flags=re.M)
    print(print_text)

def print_sys(text):
    print("\u001b[37;1m" + text + "\u001b[0m")

highlighter = lambda m: '\u001b[0m\u001b[31;1m{}\u001b[0m\u001b[37;1m'.format(m.group())

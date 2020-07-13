from utils import print_sys

def help(sh):
    """
    Command @help: prints out instructions on how to use Ouroboros
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
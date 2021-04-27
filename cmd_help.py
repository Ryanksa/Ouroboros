from utils import print_sys

def help(sh):
    """
    Command @help: Opens the help page of Ouroboros
    """
    help_str = """@exit: exit Ouroboros
@curr: switch console over to display the current note's content
@clear: erases the current note's content
@list [grouping}: list all notes, under a certain grouping if included
@drop note/[grouping}: remove notes and grouping of notes as specified. If nothing is specified remove all notes
@save note/[grouping}: save the current note into the specified notes and grouping of notes
@setgrp [grouping} note: set the grouping for the specified notes
@rename oldNoteName newNoteName: rename oldNoteName to newNoteName
@open note: opens the specified note to curr, @save will directly save this opened note
@edit note: edit the given or current (if none was given) note in edit mode
@query [grouping} 'pattern': peek all notes, under grouping if specified, with the given pattern
@peek note [grouping}: peek at the content of specified notes and groupings of notes"""
    print_sys(help_str)
    

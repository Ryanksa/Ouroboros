import re
import math

border = "=" * 128
titleFormat = lambda m: "\u001b[0m\u001b[48;5;239m" + m + "\u001b[0m\u001b[37;1m"
queryHighlight = lambda m: '\u001b[0m\u001b[31;1m{}\u001b[0m\u001b[37;1m'.format(m.group())

def print_curr(text):
    prepender = lambda m: "\u001b[32m::\u001b[0m".format(m.group())
    print_text = re.sub("^", prepender, text[:-1], flags=re.M)

    print("\u001b[32m" + border + "\u001b[0m")
    print(print_text)
    print("\u001b[32m" + border + "\u001b[0m")

def print_sys(text):
    print("\u001b[37;1m" + border + "\u001b[0m")
    print("\u001b[37;1m" + text + "\u001b[0m")
    print("\u001b[37;1m" + border + "\u001b[0m")

def print_err(text):
    print("\u001b[31;1m" + text + "\u001b[0m")

def build_title(noteGrouping, noteName):
    noteTitle = "[" + noteGrouping + "} " + noteName
    padding1 = math.floor((128-len(noteTitle))/2)
    padding2 = math.ceil((128-len(noteTitle))/2)
    noteTitle = " "*padding1 + noteTitle + " "*padding2
    return titleFormat(noteTitle)

def highlight_result(result, regex):
    return re.sub(regex, queryHighlight, result, flags=re.I)
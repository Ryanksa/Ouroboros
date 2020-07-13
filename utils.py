import re

border = "=" * 128
highlighter = lambda m: '\u001b[0m\u001b[31;1m{}\u001b[0m\u001b[37;1m'.format(m.group())

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
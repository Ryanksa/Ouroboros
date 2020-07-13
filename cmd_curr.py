import os
from utils import print_curr

def get_curr(sh):
    """
    Command @curr: switch over to the current note
    """
    os.system('cls')
    print_curr(sh.curr)
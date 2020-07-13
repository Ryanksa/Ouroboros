def exit_shell(sh):
    """
    Command @exit: exits Ouroboros
    """
    sh.cursor.close()
    sh.connection.close()
    sh.exit = True
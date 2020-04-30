from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QKeySequence

class Editor(QWidget):
    def __init__(self, file):
        super(Editor, self).__init__()
        self.file = file
        self.text = QTextEdit(self)
        self.quit_btn = QPushButton('Save and Quit')
        
        with open(file, 'r') as f:
            file_text = f.read()
            self.text.setText(file_text)
        self.init_ui()
    
    def init_ui(self):
        # place text box and button in layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.quit_btn)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.text)
        v_layout.addLayout(h_layout)
        # connect button and set shortcut
        self.quit_btn.clicked.connect(self.save_n_quit)
        self.quit_btn.setShortcut(QKeySequence("Ctrl+s"))

        # fix window size and set colors
        self.setFixedSize(1100, 700)
        self.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.text.setStyleSheet("color: rgb(211, 211, 211); font: 25px;")
        self.quit_btn.setStyleSheet("background-color: rgb(131, 131, 131);")

        # set layout and title
        self.setLayout(v_layout)
        self.setWindowTitle("@edit")
        self.show()

    def save_n_quit(self):
        with open(self.file, 'w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)
        QApplication.quit()

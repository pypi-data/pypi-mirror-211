import sys
from pymirrorui.text_comparator.comparator import TextComparator
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = TextComparator()
    window.show()
    sys.exit(app.exec_())

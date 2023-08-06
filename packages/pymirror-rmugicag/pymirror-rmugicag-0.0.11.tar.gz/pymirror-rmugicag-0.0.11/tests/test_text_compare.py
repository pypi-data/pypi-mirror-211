import unittest
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtWidgets import QApplication
from pymirror.text_comparator.comparator import TextComparator, SyntaxHighlighter


class TestTextComparator(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.window = TextComparator()

    def tearDown(self):
        self.window.close()

    def test_highlight_line(self):
        highlighter = SyntaxHighlighter(self.window.textbox1.document())
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 182, 193))
        highlighter.highlight_line(0, fmt)
        self.assertEqual(highlighter._highlight_lines[0], fmt)

    def test_clear_highlight(self):
        highlighter = SyntaxHighlighter(self.window.textbox1.document())
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 182, 193))
        highlighter.highlight_line(0, fmt)
        highlighter.clear_highlight()
        self.assertEqual(len(highlighter._highlight_lines), 0)

    # def test_highlightBlock(self):
    #     highlighter = SyntaxHighlighter(self.window.textbox1.document())
    #     fmt = QTextCharFormat()
    #     fmt.setBackground(QColor(255, 182, 193))
    #     highlighter._highlight_lines = {0: fmt}
    #     highlighter.highlightBlock('Hello\nWorld\n')
    #     expected_fmt = highlighter.currentBlock().charFormat()
    #     self.assertEqual(expected_fmt.background().color(), QColor(255, 182, 193))

    def test_show_diff(self):
        self.window.textbox1.setPlainText('hello\nworld\n')
        self.window.textbox2.setPlainText('hello\nuniverse\n')
        self.window.show_diff('left')
        expected_output = 'world'
        self.assertEqual(self.window.textbox3.toPlainText(), expected_output)

    def test_show_common_lines(self):
        self.window.textbox1.setPlainText('hello\nworld\n')
        self.window.textbox2.setPlainText('hello\nuniverse\n')
        self.window.show_common_lines()
        expected_output = 'hello'
        self.assertEqual(self.window.textbox3.toPlainText(), expected_output)

    def test_show_uncommon_lines(self):
        self.window.textbox1.setPlainText('hello\nworld\n')
        self.window.textbox2.setPlainText('hello\nuniverse\n')
        self.window.show_uncommon_lines()
        expected_output = 'world\nuniverse'
        self.assertEqual(self.window.textbox3.toPlainText(), expected_output)

    def test_highlight_lines(self):
        self.window.textbox1.setPlainText('hello\nworld\n')
        self.window.textbox2.setPlainText('hello\nuniverse\n')
        self.window.highlight_lines('diff', 'left')
        expected_fmt = self.window.textbox1_highlighter._highlight_lines[1]
        self.assertEqual(expected_fmt.background().color(), QColor(255, 182, 193))


if __name__ == '__main__':
    unittest.main()

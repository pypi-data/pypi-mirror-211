from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parnet):
        super().__init__(parnet)
        self._highlight_lines = {}

    def highlight_line(self, line_num, fmt):
        if isinstance(line_num, int) and line_num >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line_num] = fmt
            block = self.document().findBlockByLineNumber(line_num)
            self.rehighlightBlock(block)

    def clear_highlight(self):
        self._highlight_lines = {}
        self.rehighlight()

    def highlightBlock(self, text):
        blockNumber = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(blockNumber)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)


class TextComparator(QWidget):
    def __init__(self):
        super().__init__()

        # Init UI
        self.setWindowTitle('Pymirror')
        self.setGeometry(100, 100, 500, 500)

        # Create widgets
        self.textbox1 = QTextEdit(self)
        self.textbox2 = QTextEdit(self)
        self.textbox3 = QTextEdit(self)
        self.left_only_button = QPushButton('Left Only', self)
        self.right_only_button = QPushButton('Right Only', self)
        self.common_button = QPushButton('Show Common Lines', self)
        self.uncommon_button = QPushButton('Show Uncommon Lines', self)
        self.drop_duplicated_button = QPushButton('Drop duplicated', self)

        # Create textbox1 highlighter
        self.textbox1_highlighter = SyntaxHighlighter(self.textbox1.document())
        # Create textbox2 highlighter
        self.textbox2_highlighter = SyntaxHighlighter(self.textbox2.document())

        # Add event handlers for the buttons
        self.left_only_button.clicked.connect(lambda: self.show_diff("left"))
        self.right_only_button.clicked.connect(lambda: self.show_diff("right"))
        self.uncommon_button.clicked.connect(self.show_uncommon_lines)
        self.common_button.clicked.connect(self.show_common_lines)
        self.drop_duplicated_button.clicked.connect(self.drop_duplicated_lines)

        # Create layout
        main_layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        output_layout = QHBoxLayout()

        #  Add layouts
        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(output_layout)
        input_layout.addLayout(left_layout)
        input_layout.addLayout(right_layout)

        # Add widgets
        left_layout.addWidget(self.textbox1)
        right_layout.addWidget(self.textbox2)
        output_layout.addWidget(self.textbox3)
        buttons_layout.addWidget(self.left_only_button)
        buttons_layout.addWidget(self.right_only_button)
        buttons_layout.addWidget(self.common_button)
        buttons_layout.addWidget(self.uncommon_button)
        buttons_layout.addWidget(self.drop_duplicated_button)

        self.setLayout(main_layout)

    def show_diff(self, side):
        diff = ""
        text1 = self.textbox1.toPlainText().splitlines()
        text2 = self.textbox2.toPlainText().splitlines()
        if side == "left":
            diff = [line for line in text1 if line not in text2]
        if side == "right":
            diff = [line for line in text2 if line not in text1]
        self.show_text("\n".join(diff))
        self.highlight_lines("diff", side)

    def show_common_lines(self):
        text1 = self.textbox1.toPlainText().splitlines()
        text2 = self.textbox2.toPlainText().splitlines()
        common = [line for line in text1 if line in text2]
        self.show_text("\n".join(common))
        self.highlight_lines("same", "both")

    def show_uncommon_lines(self):
        text1 = self.textbox1.toPlainText().splitlines()
        text2 = self.textbox2.toPlainText().splitlines()
        uncommon1 = [line for line in text1 if line not in text2]
        uncommon2 = [line for line in text2 if line not in text1]
        uncommon = uncommon1 + uncommon2
        self.show_text("\n".join(uncommon))
        self.highlight_lines("diff", "both")

    def show_text(self, text):
        self.textbox3.clear()
        self.textbox3.append(text)

    def highlight_lines(self, operator, side):

        def iterate(lines_1, lines_2, highlighter, operation):
            for i, line in enumerate(lines_1):
                fmt = QTextCharFormat()
                if operation == "diff":
                    fmt.setBackground(QColor('white') if line in lines_2 else QColor(255, 182, 193))
                elif operation == "same":
                    fmt.setBackground(QColor(183, 217, 191) if line in lines_2 else QColor('white'))
                highlighter.highlight_line(i, fmt)

        sides = []
        self.textbox1_highlighter.clear_highlight()
        self.textbox2_highlighter.clear_highlight()
        lines1 = self.textbox1.toPlainText().splitlines()
        lines2 = self.textbox2.toPlainText().splitlines()
        if side == "left":
            sides = [(lines1, lines2, self.textbox1_highlighter)]
        elif side == "right":
            sides = [(lines2, lines1, self.textbox2_highlighter)]
        elif side == "both":
            sides = [(lines1, lines2, self.textbox1_highlighter), (lines2, lines1, self.textbox2_highlighter)]
        for s in sides:
            iterate(*s, operator)

    def drop_duplicated_lines(self):
        text1 = self.textbox1.toPlainText().splitlines()
        text2 = self.textbox2.toPlainText().splitlines()
        duplicated1 = list(set([line for line in text1 if text1.count(line) > 1]))
        duplicated2 = list(set([line for line in text2 if text2.count(line) > 1]))
        self.textbox1.setPlainText("\n".join(list(set(text1))))
        self.textbox2.setPlainText("\n".join(list(set(text2))))
        self.show_text("Left duplicates:\n" + "\n".join(duplicated1) + "\n\n" +
                       "Right duplicates:\n" + "\n".join(duplicated2))

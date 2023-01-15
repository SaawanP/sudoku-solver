from PyQt6.QtCore import Qt, QLine
from PyQt6.QtGui import QFont, QIntValidator, QPaintEvent, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QLineEdit

from sudoku_solver.cell import Cell, Location
from sudoku_solver.solver import Solver


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku Solver")
        self.setFixedSize(1000, 900)

        hlayout = QHBoxLayout()
        grid = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)

        self.start_button = QPushButton("Start Solving")
        self.start_button.clicked.connect(self.start_solve)

        hlayout.addLayout(grid, 9)
        hlayout.addWidget(self.start_button, 1)
        self.setLayout(hlayout)
        self.text_boxes = []
        for row in range(9):
            for col in range(9):
                text_box = LineEdit(row, col)
                text_box.setMinimumHeight(100)
                text_box.resize(100, 100)
                grid.addWidget(text_box, row, col)
                self.text_boxes.append(text_box)

    def start_solve(self):
        cells = {}
        for text_box in self.text_boxes:
            cell = Cell()
            if text_box.text() != "":
                text_box.given = True
                cell.options = [int(text_box.text())]
            box = text_box.row // 3 + text_box.col // 3
            location = Location(text_box.row, text_box.col, box)
            cell.location = (text_box.row, text_box.col, box)
            cells[location] = cell
        self.start_button.setDisabled(True)
        solver = Solver(cells)
        solver.solve()


class LineEdit(QLineEdit):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.given = False

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial", 20))
        self.setMaxLength(1)
        self.setValidator(QIntValidator())

    def paintEvent(self, a0: QPaintEvent):
        super().paintEvent(a0)
        painter = QPainter()
        painter.begin(self)
        thin_line = 2
        thick_line = 6
        painter.setPen(QPen(Qt.GlobalColor.black, thin_line, Qt.PenStyle.SolidLine))

        rect = self.rect()

        line = QLine(rect.topLeft(), rect.topRight())
        if self.row % 3 == 0:
            painter.setPen(QPen(Qt.GlobalColor.black, thick_line, Qt.PenStyle.SolidLine))
            painter.drawLine(line)
            painter.setPen(QPen(Qt.GlobalColor.black, thin_line, Qt.PenStyle.SolidLine))
        else:
            painter.drawLine(line)

        line = QLine(rect.topLeft(), rect.bottomLeft())
        if self.col % 3 == 0:
            painter.setPen(QPen(Qt.GlobalColor.black, thick_line, Qt.PenStyle.SolidLine))
            painter.drawLine(line)
            painter.setPen(QPen(Qt.GlobalColor.black, thin_line, Qt.PenStyle.SolidLine))
        else:
            painter.drawLine(line)

        painter.setPen(QPen(Qt.GlobalColor.black, thick_line, Qt.PenStyle.SolidLine))
        if self.row == 8:
            line = QLine(rect.bottomLeft(), rect.bottomRight())
            painter.drawLine(line)
        if self.col == 8:
            line = QLine(rect.topRight(), rect.bottomRight())
            painter.drawLine(line)
        painter.end()

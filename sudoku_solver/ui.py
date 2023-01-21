import os
from typing import Dict

from PyQt6.QtCore import Qt, QLine
from PyQt6.QtGui import QFont, QIntValidator, QPaintEvent, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QLineEdit

from sudoku_solver.cell import Cell, Location
import sudoku_solver.solver as solver


class LineEdit(QLineEdit):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial", 20))
        self.setMaxLength(1)
        self.setValidator(QIntValidator())

    def paintEvent(self, a0: QPaintEvent):
        super().paintEvent(a0)
        painter = QPainter()
        painter.begin(self)
        thin_line = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        thick_line = QPen(Qt.GlobalColor.black, 6, Qt.PenStyle.SolidLine)
        painter.setPen(thin_line)

        rect = self.rect()

        line = QLine(rect.topLeft(), rect.topRight())
        if self.row % 3 == 0:
            painter.setPen(thick_line)
            painter.drawLine(line)
            painter.setPen(thin_line)
        else:
            painter.drawLine(line)

        line = QLine(rect.topLeft(), rect.bottomLeft())
        if self.col % 3 == 0:
            painter.setPen(thick_line)
            painter.drawLine(line)
            painter.setPen(thin_line)
        else:
            painter.drawLine(line)

        painter.setPen(thick_line)
        if self.row == 8:
            line = QLine(rect.bottomLeft(), rect.bottomRight())
            painter.drawLine(line)
        if self.col == 8:
            line = QLine(rect.topRight(), rect.bottomRight())
            painter.drawLine(line)
        painter.end()


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
        self.text_boxes: Dict[Location, LineEdit] = {}
        for row in range(9):
            for col in range(9):
                text_box = LineEdit(row, col)
                text_box.setMinimumHeight(100)
                text_box.resize(100, 100)
                grid.addWidget(text_box, row, col)
                box = row // 3 * 3 + col // 3
                location = Location(row, col, box)
                self.text_boxes[location] = text_box

        if os.path.exists("file.txt"):
            with open("file.txt", "r") as f:
                for row, rows in enumerate(f.readlines()):
                    for col, digit in enumerate(rows):
                        if digit not in [" ", "\n"]:
                            box = int(row) // 3 * 3 + int(col) // 3
                            self.text_boxes[(int(row), int(col), box)].setText(digit)

    def create_file(self):
        with open("file.txt", "w") as f:
            for row in range(9):
                text_row = ""
                for col in range(9):
                    box = row // 3 * 3 + col // 3
                    text_box = self.text_boxes[(row, col, box)]
                    text = text_box.text()
                    if text == "":
                        text = " "
                    text_row += text
                f.writelines(text_row)
                f.write("\n")

    def start_solve(self):
        self.create_file()

        cells = {}
        first_cells = []
        for location, text_box in self.text_boxes.items():
            cell = Cell()
            cell.location = location
            if text_box.text() != "":
                text_box.given = True
                cell.options = {int(text_box.text())}
                first_cells.append(cell)
            cells[location] = cell
        self.start_button.setDisabled(True)
        solver.create_cycles(cells, first_cells)
        for cell in solver.solve(cells):
            self.text_boxes[cell.location].setText(f"{list(cell.options)[0]}")

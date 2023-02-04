import os
from typing import Dict, List, Generator, Tuple, Optional

from PyQt6.QtCore import Qt, QLine, QPointF, QRectF
from PyQt6.QtGui import QFont, QIntValidator, QPaintEvent, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel

from sudoku_solver.cell import Cell, Location
import sudoku_solver.solver as solver


class LineEdit(QLineEdit):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.given = True
        self.complete = False
        self.options = {}

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Arial", 20))
        self.setMaxLength(1)
        self.setValidator(QIntValidator())
        self.active = False

    def paintEvent(self, a0: QPaintEvent):
        back_color = "white"
        if self.active:
            back_color = "yellow"

        fore_color = "blue"
        if self.given:
            fore_color = "black"
        self.setStyleSheet(f"background-color: {back_color}; color: {fore_color}")
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

        if not self.complete:
            painter.setPen(QPen(Qt.GlobalColor.darkGray, 6, Qt.PenStyle.SolidLine))
            for option in self.options:
                pos_x = rect.center().x() + ((option-1) % 3 - 1) * rect.width() / 3 - 8
                pos_y = rect.center().y() + ((option-1) // 3 - 1) * rect.height() / 3 + 9
                text_rect = QRectF()
                painter.drawText(QPointF(pos_x, pos_y), str(option))
        painter.end()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sudoku Solver")
        self.last_cell_location = None

        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        grid = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)

        self.start_button = QPushButton("Start Solving")
        self.start_button.clicked.connect(self.start_solve)

        self.solve_path: Optional[Generator[Tuple[List[Cell], str]]] = None
        self.next_button = QPushButton("Next Step")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setDisabled(True)

        self.display_text = QLabel()
        self.display_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_text.setWordWrap(True)
        self.display_text.setFont(QFont("Arial", 20))
        self.display_text.setText("This is some test text to see the spacing of the label")
        self.display_text.setMaximumSize(300, 300)
        vlayout.addWidget(self.display_text, 1)
        vlayout.addWidget(self.start_button, 1)
        vlayout.addWidget(self.next_button, 1)

        hlayout.addLayout(grid, 9)
        hlayout.addLayout(vlayout, 3)
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

        if os.path.exists("examples/simple.txt"):
            with open("examples/simple.txt", "r") as f:
                for row, rows in enumerate(f.readlines()):
                    for col, digit in enumerate(rows):
                        if digit not in [" ", "\n"]:
                            box = int(row) // 3 * 3 + int(col) // 3
                            self.text_boxes[(int(row), int(col), box)].setText(digit)

    def next_step(self):
        if self.last_cell_location:
            self.text_boxes[self.last_cell_location].active = False
        try:
            cells, text = next(self.solve_path)
            for cell in cells:
                if cell.completed:
                    self.text_boxes[cell.location].complete = True
                    self.text_boxes[cell.location].setText(f"{list(cell.options)[0]}")
                self.display_text.setText(text)
                self.text_boxes[cell.location].options = cell.options
                self.text_boxes[cell.location].active = True
                self.text_boxes[cell.location].setDisabled(True)
                self.last_cell_location = cell.location
        except StopIteration:
            self.display_text.setText("Puzzle has been completed")

    def create_file(self):
        with open("examples/simple.txt", "w") as f:
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
                text_box.setDisabled(True)
                cell.options = {int(text_box.text())}
                first_cells.append(cell)
                text_box.complete = True
            else:
                text_box.given = False
            cells[location] = cell
            text_box.options = cell.options
        self.start_button.setDisabled(True)
        solver.create_cycles(cells, first_cells)
        self.solve_path = (solver.solve(cells))
        self.next_button.setDisabled(False)

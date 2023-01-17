import copy
from typing import Dict, List, NamedTuple, Optional

Location = NamedTuple("Location", [("row", int), ("col", int), ("box", int)])


class Cell:
    def __init__(self):
        self.options = {i for i in range(1, 10)}
        self.location: Location = (0, 0, 0)
        self.row_cycles: Dict[int, List[Cell]] = {}
        self.col_cycles: Dict[int, List[Cell]] = {}
        self.box_cycles: Dict[int, List[Cell]] = {}

    def remove_option(self, value: int):
        for cell in self.row_cycles[value]:
            cell.row_cycles[value].remove(self)
        del self.row_cycles[value]

        for cell in self.col_cycles[value]:
            cell.col_cycles[value].remove(self)
        del self.col_cycles[value]

        for cell in self.box_cycles[value]:
            cell.box_cycles[value].remove(self)
        del self.box_cycles[value]

        self.options.remove(value)

    def complete_cell(self, value: int):
        for cells in self.row_cycles.values():
            cells = copy.copy(cells)
            for cell in cells:
                cell.remove_option(value)

        for cells in self.col_cycles.values():
            cells = copy.copy(cells)
            for cell in cells:
                cell.remove_option(value)

        for cells in self.box_cycles.values():
            cells = copy.copy(cells)
            for cell in cells:
                cell.remove_option(value)

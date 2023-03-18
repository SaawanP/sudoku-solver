import copy
from typing import Dict, List, NamedTuple, Set

Location = NamedTuple("Location", [("row", int), ("col", int), ("box", int)])


class Cell:
    def __init__(self):
        self.options = {i for i in range(1, 10)}
        self.completed = False
        self.location: Location = (0, 0, 0)
        self.row_cycles: Dict[int, List[Cell]] = {}
        self.col_cycles: Dict[int, List[Cell]] = {}
        self.box_cycles: Dict[int, List[Cell]] = {}
        self.perm_row_cycles: Set[Cell] = set()
        self.perm_col_cycles: Set[Cell] = set()
        self.perm_box_cycles: Set[Cell] = set()
        self.last_pattern = None

    def remove_option(self, value: int):
        if value not in self.options:
            return

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
        for attr in ["row_cycles", "col_cycles", "box_cycles"]:
            for cells in self.__getattribute__(attr).values():
                connected_cells = copy.copy(cells)
                for cell in connected_cells:
                    cell.remove_option(value)
                    cell.remove_connected_cell(self)
            self.__setattr__(attr, {value: []})

        self.options = {value}
        self.completed = True

    def clean_options_except(self, valid_options: List[int]):
        for option in copy.copy(self.options):
            if option not in valid_options:
                self.remove_option(option)

    def remove_connected_cell(self, cell):
        for attr in ["row_cycles", "col_cycles", "box_cycles"]:
            for cells in self.__getattribute__(attr).values():
                if cell in cells:
                    cells.remove(cell)

    def print_location_of_connected_cells(self, attr, value):
        for linked_cell in self.__getattribute__(attr)[value]:
            print(linked_cell.location, end=", ")
        print()

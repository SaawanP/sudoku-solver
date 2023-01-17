import copy
from inspect import ismethod
from typing import Dict, List, NamedTuple, Optional

Location = NamedTuple("Location", [("row", int), ("col", int), ("box", int)])
Notification = NamedTuple("Notification", [("location", Location), ("values", List[int])])


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

    def find_possible_action(self) -> Optional[Notification]:
        for func in Patterns.get_all_patterns():
            a = func(self)
            if a is not None:
                return Notification(self.location, a)


class Patterns:
    @staticmethod
    def get_all_patterns():
        return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__") and i != "get_all_patterns")

    @staticmethod
    def naked_single(cell: Cell) -> Optional[List[int]]:
        return None

    @staticmethod
    def hidden_single(cell: Cell) -> Optional[List[int]]:
        return None

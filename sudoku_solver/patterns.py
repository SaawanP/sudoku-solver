from typing import Generator, Callable

from sudoku_solver.cell import Cell, Location


def get_all_patterns() -> Generator:
    return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__"))


class Patterns:

    # TODO try to generalize hidden and naked collections
    #  to four in order to make a common function that is called within each func
    @staticmethod
    def a_naked_single(cell: Cell):
        text = lambda loc, val: f"A naked single '{val}' found at row {loc.row + 1}, col {loc.col + 1}, box {loc.box + 1}"
        if len(cell.options) == 1:
            option = list(cell.options)
            return option, (True, True, True), [cell], text(cell.location, option[0])
        return None, None, None, None

    @staticmethod
    def b_hidden_single(cell: Cell):
        text = lambda loc, val: f"In box {loc.box}, the only one cell can host a {val} is row {loc.row}, col {loc.col}"
        def check_attr(attr):
            for val, linked_cells in cell.__getattribute__(attr).items():
                if len(linked_cells) == 1:
                    return [val], (True, True, True), [cell], text(cell.location, val)

        attrs = ["row_cycles", "col_cycles", "box_cycles"]
        for a in attrs:
            check_attr(a)
        return None, None, None, None

    @staticmethod
    def c_naked_double(cell: Cell):
        return None, None, None, None

    @staticmethod
    def d_hidden_double(cell: Cell):
        return None, None, None, None

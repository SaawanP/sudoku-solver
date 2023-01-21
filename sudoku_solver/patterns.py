from typing import Optional, List, Tuple, Union

from sudoku_solver.cell import Cell


def get_all_patterns():
    return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__"))


class Patterns:

    # TODO try to generalize hidden and naked collections
    #  to four in order to make a common function that is called within each func
    @staticmethod
    def a_naked_single(cell: Cell):
        if len(cell.options) == 1:
            print(cell.location, "naked single", cell.options)
            return list(cell.options), (True, True, True), [cell]
        return None, None, None

    @staticmethod
    def b_hidden_single(cell: Cell):
        def check_attr(attr):
            for val, linked_cells in cell.__getattribute__(attr).items():
                if len(linked_cells) == 1:
                    return [val], (True, True, True), [cell]

        attrs = ["row_cycles", "col_cycles", "box_cycles"]
        for a in attrs:
            check_attr(a)
        return None, None, None

    @staticmethod
    def c_naked_double(cell: Cell):
        return None, None, None

    @staticmethod
    def d_hidden_double(cell: Cell):
        return None, None, None

from typing import Generator, Callable

import numpy as np

from sudoku_solver.cell import Cell, Location


def get_all_patterns() -> Generator:
    return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__"))


class Patterns:

    # TODO try to generalize hidden and naked collections
    #  to four in order to make a common function that is called within each func

    # TODO realization the naked and single collections can be combined since they follow the same logic when they are
    #  generalized, see naked double and hidden double to realize again, return is handled differently
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
                if len(linked_cells) == 0:
                    return [val], (True, True, True), [cell], text(cell.location, val)
            return None, None, None, None

        for a in ["row_cycles", "col_cycles", "box_cycles"]:
            ret = check_attr(a)
            if None not in ret:
                return ret
        return None, None, None, None

    @staticmethod
    def c_naked_double(cell: Cell):
        text = "hi"

        def check_attr(attr, cells):
            prev_linked_cells = []
            for val, linked_cells in cell.__getattribute__(attr).items():
                correct_length = len(linked_cells) == 1
                same_linked_cells = linked_cells == prev_linked_cells
                if correct_length and same_linked_cells:
                    cells = [cell] + prev_linked_cells
                    return True
                prev_linked_cells = linked_cells
            return False

        involved_cells = None
        if len(cell.options) == 2:
            valid_directions = [False, False, False]
            for i, a in enumerate(["row_cycles", "col_cycles", "box_cycles"]):
                valid_directions[i] = check_attr(a, involved_cells)
            if np.any(valid_directions):
                return list(cell.options), valid_directions, involved_cells, text

        return None, None, None, None

    @staticmethod
    def d_hidden_double(cell: Cell):
        """
        need fixing

        :param cell:
        :return:
        """
        text = "hi"

        def check_attr(attr, cells):
            prev_linked_cells = []
            connected_values = []
            for val, linked_cells in cell.__getattribute__(attr).items():
                correct_length = len(linked_cells) == 1
                same_linked_cells = linked_cells == prev_linked_cells
                if correct_length and same_linked_cells:
                    cells = [cell] + prev_linked_cells
                    connected_values.append(val)
                    return True
                prev_linked_cells = linked_cells
            return False

        involved_cells = None
        valid_directions = [False, False, False]
        for i, a in enumerate(["row_cycles", "col_cycles", "box_cycles"]):
            valid_directions[i] = check_attr(a, involved_cells)
            if np.any(valid_directions):
                return list(cell.options), valid_directions, involved_cells, text

        return None, None, None, None

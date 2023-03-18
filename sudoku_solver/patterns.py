from typing import Generator, Callable

import numpy as np

from sudoku_solver.cell import Cell, Location


def get_all_patterns() -> Generator:
    return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__"))


class Patterns:
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
                    cell.complete_cell(val)
                    return [val], (True, True, True), [cell], text(cell.location, val)
            return None, None, None, None

        for a in ["row_cycles", "col_cycles", "box_cycles"]:
            ret = check_attr(a)
            if None not in ret:
                return ret
        return None, None, None, None

    @staticmethod
    def c_naked_double(cell: Cell):
        text = "Naked Double"

        def check_attr(attr):
            linked_cells_sets = []
            for val, linked_cells in cell.__getattribute__(attr).items():
                linked_cells_sets.append(set(linked_cells))
            common_cells = linked_cells_sets[0].intersection(*linked_cells_sets)
            for common_cell in common_cells:
                if len(common_cell.options) == 2:
                    return True, [cell, common_cell]
            return False

        involved_cells = None
        valid_directions = [False, False, False]
        if len(cell.options) == 2:
            for i, a in enumerate(["row_cycles", "col_cycles", "box_cycles"]):
                ret = check_attr(a)
                valid_directions[i] = ret
                if type(ret) == tuple:
                    valid_directions[i] = ret[0]
                    involved_cells = ret[1]
            if np.any(valid_directions):
                return list(cell.options), valid_directions, involved_cells, text

        return None, None, None, None

    @staticmethod
    def d_hidden_double(cell: Cell):
        text = "Hidden Double"

        def check_attr(attr):
            prev_linked_cells = []
            connected_values = []
            for val, linked_cells in cell.__getattribute__(attr).items():
                # this checks for the connected cell and this can be generalized
                if len(linked_cells) == 1:
                    if [cell] + linked_cells == prev_linked_cells:
                        return True, prev_linked_cells
                    prev_linked_cells = [cell] + linked_cells
            return False

        involved_cells = None
        valid_directions = [False, False, False]
        for i, a in enumerate(["row_cycles", "col_cycles", "box_cycles"]):
            ret = check_attr(a)
            valid_directions[i] = ret
            if type(ret) == tuple:
                valid_directions[i] = ret[0]
                involved_cells = ret[1]
        if np.any(valid_directions):
            return list(cell.options), valid_directions, involved_cells, text

        return None, None, None, None

    @staticmethod
    def e_locked_candidate(cell: Cell):
        return None, None, None, None

    @staticmethod
    def f_x_wing(cell: Cell):
        return None, None, None, None

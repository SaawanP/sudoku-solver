from typing import Dict, List, Optional, Tuple

from sudoku_solver.cell import Cell, Location
from sudoku_solver.patterns import Patterns


def print_cycles(cells: Dict[Location, Cell]):
    for cell in cells.values():
        print(f"Current cell: {cell.location}")
        print(f"Options: {cell.options}")
        for i in cell.options:
            print(f"\tOptions {i} cycles: ")
            s = ""
            for j in cell.row_cycles[i]:
                s += str(j.location) + ", "
            print(f"\t\tRow: {s}")
            s = ""
            for j in cell.col_cycles[i]:
                s += str(j.location) + ", "
            print(f"\t\tCol: {s}")
            s = ""
            for j in cell.box_cycles[i]:
                s += str(j.location) + ", "
            print(f"\t\tBox: {s}")

        response = input("Continue (y/n)")
        while response in ["Y", "y", "N", "n"]:
            response = input("Continue (y/n)")
        if response in ["N", "n"]:
            return


def solve(cells: Dict[Location, Cell]):
    while True:
        values: Optional[List[int]] = None
        affected_directions: Optional[Tuple[bool, bool, bool]] = None
        for pattern in Patterns.get_all_patterns():
            for cell in cells.values():
                values, affected_directions = pattern(cell)
                if values is not None:
                    break
        if values is None:
            break

        # -1 in affected_directions means that coordinate does not matter
        relevant_cycles = ["row_cycles", "col_cycles", "box_cycles"]
        if affected_directions[0]:
            relevant_cycles.remove("row_cycles")
        if affected_directions[1]:
            relevant_cycles.remove("col_cycles")
        if affected_directions[2]:
            relevant_cycles.remove("box_cycles")

        cell = cells[affected_directions]
        for cycle in relevant_cycles:
            for val in values:
                linked_cells: List[Cell] = cell.__getattribute__(cycle)[val]
                for linked_cell in linked_cells:
                    linked_cell.remove_option(val)

    print("Complete")


def create_cycles(cells: Dict[Location, Cell], first_cells: List[Cell]):
    def link_cells(common_cells: List[Cell], attr):
        for cell in common_cells:
            common_digits = curr_cell.options & cell.options
            for i in common_digits:
                curr_cell.__getattribute__(attr).setdefault(i, []).append(cell)
                cell.__getattribute__(attr).setdefault(i, []).append(curr_cell)
        common_cells.append(curr_cell)

    cols_common_cells: List[List[Cell]] = [[] for i in range(9)]
    boxes_common_cells: List[List[Cell]] = [[] for i in range(9)]
    for row in range(9):
        row_common_cells: List[Cell] = []
        for col in range(9):
            box = row // 3 * 3 + col // 3
            col_common_cells = cols_common_cells[col]
            box_common_cells = boxes_common_cells[box]
            curr_cell = cells[(row, col, box)]
            link_cells(row_common_cells, "row_cycles")
            link_cells(col_common_cells, "col_cycles")
            link_cells(box_common_cells, "box_cycles")

    for cell in first_cells:
        cell.complete_cell(list(cell.options)[0])

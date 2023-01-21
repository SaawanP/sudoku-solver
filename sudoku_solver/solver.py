from typing import Dict, List, Optional, Tuple, Set

from sudoku_solver.cell import Cell, Location
from sudoku_solver.patterns import get_all_patterns


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
        location: Optional[Location] = None
        involved_cells: List[Cell] = []

        # apply the different sudoku patterns to the cells and does them in increasing difficulty
        for pattern in get_all_patterns():
            for cell in cells.values():
                # print(cell.location, cell.completed, pattern)
                if not cell.completed:
                    values, affected_directions, involved_cells = pattern(cell)
                    if values is not None:
                        print(values)
                        location = cell.location
                        break
            else:
                continue
            break
        if values is None:
            print("hi")
            break

        # -1 in affected_directions means that coordinate does not matter
        relevant_cycles = ["row_cycles", "col_cycles", "box_cycles"]
        if not affected_directions[0]:
            relevant_cycles.remove("row_cycles")
        if not affected_directions[1]:
            relevant_cycles.remove("col_cycles")
        if not affected_directions[2]:
            relevant_cycles.remove("box_cycles")
        # TODO might need to remove all other options in involved cells
        linked_cells: List[Set[Cell]] = [set(), set(), set()]
        for i, cycle in enumerate(relevant_cycles):
            for cell in involved_cells:
                cell.completed = True
                for val in values:
                    for linked_cell in cell.__getattribute__(cycle)[val]:
                        if linked_cell not in linked_cells[i] and linked_cell not in involved_cells:
                            linked_cells[i].add(linked_cell)
                    for linked_cell in linked_cells[i]:
                        linked_cell.remove_option(val)
        print("yielding")
        yield involved_cells[0]


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

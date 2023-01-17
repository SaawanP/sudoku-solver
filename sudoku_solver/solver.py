from queue import Queue
from typing import Dict, List

from sudoku_solver.util import Cell, Location


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
        if response in ["N", "n"]:
            return


def solve(cells: Dict[Location, Cell]):
    while True:
        notification_queue = Queue()
        for cell in cells.values():
            new_action = cell.find_possible_action()
            if new_action is not None:
                notification_queue.put(new_action)
        if len(notification_queue.queue) == 0:
            break
        notification = notification_queue.get()

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

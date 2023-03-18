from typing import Dict, List, Optional, Tuple, Set

from sudoku_solver.cell import Cell, Location
from sudoku_solver.patterns import get_all_patterns


def print_cycles(cells: Dict[Location, Cell], check_only_cells: List[Cell] = []):
    for cell in cells.values():
        if cell not in check_only_cells:
            continue
        print(f"Current cell: {cell.location}")
        print(f"Options: {cell.options}")
        for i in cell.options:
            print(f"\tOption {i} cycles: ")
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
        while response not in ["Y", "y", "N", "n"]:
            response = input("Continue (y/n)")
        if response in ["N", "n"]:
            return


def solve(cells: Dict[Location, Cell]) -> Tuple[List[Cell], str]:
    while True:
        values: Optional[List[int]] = None
        affected_directions: Optional[Tuple[bool, bool, bool]] = None
        function_text: str = ""
        involved_cells: List[Cell] = []

        check_cell_location = Location(2, 0, 0)
        check_cells = []

        # apply the different sudoku patterns to the cells and does them in increasing difficulty
        for pattern in get_all_patterns():
            for cell in cells.values():
                # TODO find out why the 1 8 pair in row 2 (0 index) keeps getting checked
                # this is because there is some improper clean up

                # TODO I dont like this will make better solution later
                if cell.last_pattern in [pattern.__name__.replace("d_hidden", "c_naked"),
                                         pattern.__name__.replace("c_naked", "d_hidden")]:
                    continue
                if cell.completed:
                    continue
                print(pattern, cell.location)
                values, affected_directions, involved_cells, function_text = pattern(cell)
                if values is not None:
                    for involved_cell in involved_cells:
                        involved_cell.last_pattern = pattern.__name__
                    if cell.location == check_cell_location:
                        check_cells = involved_cells
                    break
            else:  # this else statement for the for loop is used as a super break to leave both for loops
                continue
            break
        if values is None:
            break

        relevant_cycles = ["row_cycles", "col_cycles", "box_cycles"]
        if not affected_directions[0]:
            relevant_cycles.remove("row_cycles")
        if not affected_directions[1]:
            relevant_cycles.remove("col_cycles")
        if not affected_directions[2]:
            relevant_cycles.remove("box_cycles")

        print_cycles(cells, check_cells)
        if len(involved_cells) == 1:
            involved_cells[0].complete_cell(values[0])
        else:
            print(relevant_cycles)
            print([cell.location for cell in involved_cells])
            for cycle in relevant_cycles:
                for cell in involved_cells:
                    for val in values:
                        cell.print_location_of_connected_cells(cycle, val)
                        for linked_cell in cell.__getattribute__(cycle)[val]:
                            print(linked_cell.location, cycle)
                            if linked_cell not in involved_cells:
                                linked_cell.remove_option(val)
                    cell.clean_options_except(values)
        yield involved_cells, function_text


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
    rows_common_cells: List[List[Cell]] = [[] for i in range(9)]
    for row in range(9):
        for col in range(9):
            box = row // 3 * 3 + col // 3
            row_common_cells = rows_common_cells[row]
            col_common_cells = cols_common_cells[col]
            box_common_cells = boxes_common_cells[box]
            curr_cell = cells[(row, col, box)]
            link_cells(row_common_cells, "row_cycles")
            link_cells(col_common_cells, "col_cycles")
            link_cells(box_common_cells, "box_cycles")

    for cell in cells.values():
        cell.perm_col_cycles = set(cols_common_cells[cell.location.col])
        cell.perm_row_cycles = set(rows_common_cells[cell.location.row])
        cell.perm_box_cycles = set(boxes_common_cells[cell.location.box])

    for cell in first_cells:
        cell.complete_cell(list(cell.options)[0])


def check_complete(starting_cell: Cell):
    current_stack: List[Cell] = []  # used to avoid inf cycles
    # TODO avoid multiple checks of the same cycle
    # ie 1 2 3, some time later 1 3 2 will be checked
    for cycle in ["perm_row_cycles", "perm_col_cycles", "perm_box_cycles"]:
        connected_cells: Set[Cell] = starting_cell.__getattribute__(cycle)
        for connected_cell in connected_cells:
            pass

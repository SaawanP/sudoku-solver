from typing import Optional, List, Tuple

from sudoku_solver.cell import Cell


class Patterns:
    @staticmethod
    def get_all_patterns():
        return (getattr(Patterns, i) for i in dir(Patterns) if not i.startswith("__") and i != "get_all_patterns")

    @staticmethod
    def naked_single(cell: Cell) -> Optional[Tuple[List[int], Tuple[bool, bool, bool]]]:
        return None

    @staticmethod
    def hidden_single(cell: Cell) -> Optional[Tuple[List[int], Tuple[bool, bool, bool]]]:
        return None

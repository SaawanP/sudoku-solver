from collections import namedtuple
from typing import Tuple, Dict, List

Location = namedtuple("Location", ["row", "col", "box"])


class Cell:
    def __init__(self):
        self.options = {i for i in range(1, 10)}
        self.location: Location = (0, 0, 0)
        self.row_cycles: Dict[int, List[Cell]] = {}
        self.col_cycles: Dict[int, List[Cell]] = {}
        self.box_cycles: Dict[int, List[Cell]] = {}

    def remove_option(self, value: int):
        pass

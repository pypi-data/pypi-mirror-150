"""HEP Dataframe"""
from __future__ import annotations

import awkward as ak

# import numpy as np


class HEPDataframe:
    """HEP Dataframe"""

    def __init__(self, data: ak.Record) -> None:
        """Define a HEPDataframe."""
        if not isinstance(data, ak.Record):
            raise TypeError("Events should be an 'awkward.Record'.")
        self.data = data

    @property
    def my_property(self) -> ak.Record:
        """My property."""
        return self.data.x + 1


def main() -> None:
    """HEP Dataframe - Main"""
    my_array = ak.Record({"x": [1, 2, 3]})
    # my_array = ak.Array({"x": [1, 2, 3]})
    print(HEPDataframe(my_array).my_property)


if __name__ == "__main__":
    main()
    # print(type(ak.Array({"x": [1, 2, 3]})))

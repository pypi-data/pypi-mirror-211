from __future__ import annotations

from typing import Literal, Optional

from atoti_core import ColumnCoordinates, Condition, Constant

Restriction = Condition[
    ColumnCoordinates,
    Literal["eq", "isin"],
    Constant,
    Optional[Literal["and"]],
]

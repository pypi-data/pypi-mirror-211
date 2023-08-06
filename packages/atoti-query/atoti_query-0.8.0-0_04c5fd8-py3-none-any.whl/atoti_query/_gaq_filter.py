from __future__ import annotations

from typing import Literal, Optional, Union

from atoti_core import Condition, Constant, HierarchyCoordinates, LevelCoordinates

GaqFilter = Condition[
    Union[HierarchyCoordinates, LevelCoordinates],
    Literal["eq", "isin"],
    Constant,
    Optional[Literal["and"]],
]

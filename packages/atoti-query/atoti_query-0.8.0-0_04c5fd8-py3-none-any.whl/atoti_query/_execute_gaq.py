from collections.abc import Iterable
from datetime import timedelta
from typing import Optional, Protocol

import pandas as pd
from atoti_core import LevelCoordinates, MeasureCoordinates

from ._gaq_filter import GaqFilter


class ExecuteGaq(Protocol):
    def __call__(
        self,
        *,
        cube_name: str,
        filter: Optional[GaqFilter] = None,  # noqa: A002
        include_empty_rows: bool,
        include_totals: bool,
        levels_coordinates: Iterable[LevelCoordinates],
        measures_coordinates: Iterable[MeasureCoordinates],
        scenario: str,
        timeout: timedelta,
    ) -> pd.DataFrame:
        ...

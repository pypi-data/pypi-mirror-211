from collections.abc import Iterable
from typing import Protocol

from atoti_core import CoordinatesT, DataType


class GetDataTypes(Protocol):
    def __call__(
        self, coordinates: Iterable[CoordinatesT], /, *, cube_name: str
    ) -> dict[CoordinatesT, DataType]:
        ...

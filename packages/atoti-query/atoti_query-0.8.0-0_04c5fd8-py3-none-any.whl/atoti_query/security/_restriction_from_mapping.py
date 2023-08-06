from __future__ import annotations

from collections.abc import Mapping, Sequence

from atoti_core import ColumnCoordinates, Constant, IsinCondition, combine_conditions

from ._restriction import Restriction


def restriction_from_mapping(
    restriction: Mapping[str, Mapping[str, Sequence[str]]], /
) -> Restriction:
    conditions = [
        IsinCondition[ColumnCoordinates, Constant](
            subject=ColumnCoordinates(table_name, column_name),
            elements=tuple(Constant(element) for element in elements),
        ).normalized
        for table_name, column_restriction in restriction.items()
        for column_name, elements in column_restriction.items()
    ]
    return combine_conditions((conditions,))

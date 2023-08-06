from __future__ import annotations

from atoti_core import ColumnCoordinates, Constant, decombine_condition

from ._restriction import Restriction


def _get_restricted_element(constant: Constant, /) -> str:
    value = constant.value

    if not isinstance(value, str):
        raise TypeError(
            f"Expected restricted element to be a string but got `{value}` of type `{type(value)}`."
        )

    return value


def restriction_to_dict(restriction: Restriction, /) -> dict[str, dict[str, list[str]]]:
    result: dict[str, dict[str, list[str]]] = {}

    comparison_conditions, isin_conditions, _ = decombine_condition(
        restriction,
        allowed_subject_types=(ColumnCoordinates,),
        allowed_comparison_operators=("eq",),
        allowed_target_types=(Constant,),
        allowed_combination_operators=("and",),
        allowed_isin_element_types=(Constant,),
    )[0]

    for comparison_condition in comparison_conditions:
        result.setdefault(comparison_condition.subject.table_name, {})[
            comparison_condition.subject.column_name
        ] = [_get_restricted_element(comparison_condition.target)]

    for isin_condition in isin_conditions:
        result.setdefault(isin_condition.subject.table_name, {})[
            isin_condition.subject.column_name
        ] = [_get_restricted_element(element) for element in isin_condition.elements]

    return result

from typing import Union

from atoti_core import (
    ColumnCoordinates,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    Constant,
    ConstantValue,
    decombine_condition,
)

_AndDict = dict[str, dict[str, Union[ConstantValue, list[ConstantValue]]]]

_JsonSerializableDict = Union[_AndDict, dict[str, list[_AndDict]]]


def condition_to_json_serializable_dict(
    condition: Condition[
        ColumnCoordinates,
        ConditionComparisonOperatorBound,
        Constant,
        ConditionCombinationOperatorBound,
    ]
) -> _JsonSerializableDict:
    and_dicts: list[_AndDict] = []

    for or_condition in decombine_condition(  # type: ignore[var-annotated]
        condition,
        allowed_isin_element_types=(Constant,),
        allowed_subject_types=(ColumnCoordinates,),
        allowed_target_types=(Constant,),
    ):
        and_dict: _AndDict = {}
        comparison_conditions, isin_conditions, *_ = or_condition

        for comparison_condition in comparison_conditions:
            column_name = comparison_condition.subject.column_name
            operator = (
                "lte"
                if comparison_condition.operator == "le"
                else "gte"
                if comparison_condition.operator == "ge"
                else comparison_condition.operator
            )
            and_dict.setdefault(column_name, {})[
                f"${operator}"
            ] = comparison_condition.target.value

        for isin_condition in isin_conditions:
            column_name = isin_condition.subject.column_name
            and_dict.setdefault(column_name, {})["$in"] = [
                element.value for element in isin_condition.elements
            ]

        and_dicts.append(and_dict)

    if len(and_dicts) == 1:
        return and_dicts[0]

    return {"$or": and_dicts}

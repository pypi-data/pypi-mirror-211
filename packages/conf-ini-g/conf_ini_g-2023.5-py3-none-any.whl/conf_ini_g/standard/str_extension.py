# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import ast as asgt
import dataclasses as dtcl
import textwrap as text
from types import GenericAlias, UnionType
from typing import Any, Iterable, Sequence

from conf_ini_g.standard.type_extension import (
    HintTreeFromTypeHint,
    hint_node_t,
    none_t,
    raw_hint_h,
)


TRUE_VALUES = ("true", "yes", "on")
FALSE_VALUES = ("false", "no", "off")


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _value_node_t:
    consolidated: Any
    type: type | None = None
    elements: tuple[_value_node_t, ...] | None = None

    def __post_init__(self) -> None:
        """"""
        self.type = type(self.consolidated)


def Flattened(string: str, /) -> str:
    """"""
    return text.dedent(string).replace("\n", "; ")


def AlignedOnSeparator(
    string: str | Sequence[str], separator: str, replacement: str, /
) -> str | tuple[str, ...] | list[str]:
    """"""
    if should_return_str := isinstance(string, str):
        lines = string.splitlines()
    else:
        lines = string
    indices = tuple(_lne.find(separator) for _lne in lines)
    longest = max(indices)

    output = (
        _lne.replace(separator, (longest - _lgt) * " " + replacement, 1)
        if _lgt > 0
        else _lne
        for _lne, _lgt in zip(lines, indices)
    )
    if should_return_str:
        return "\n".join(output)
    elif isinstance(string, tuple):
        return tuple(output)
    else:
        return list(output)


def AsInterpretedObject(
    string: str, /, *, expected_type: type | None = None
) -> tuple[Any, bool]:
    """
    expected_type: Must not be passed explicitly as None since None is interpreted as
    "no specific expected type". When expecting None, pass none_t.
    """
    if expected_type is None:
        try:
            value = asgt.literal_eval(string)
        except (SyntaxError, ValueError):
            value = string

        return value, True

    failed_interpretation = None, False
    lowered = string.lower()

    if expected_type is none_t:
        return None, (lowered == "none")

    if expected_type is bool:
        if lowered in TRUE_VALUES:
            return True, True
        if lowered in FALSE_VALUES:
            return False, True
        return failed_interpretation

    # The expected type might be instantiable from a string, e.g.: float("1.0").
    # However, a success does not mean that the interpretation is valid, e.g.:
    # tuple("(1, 2, 3)"). To confirm that a success is indeed a correct interpretation,
    # the string representation of the interpreted value is compared with the string.
    # This is not a perfect test, so "literal_eval" might still be called below.
    try:
        value = expected_type(string)
        success = str(value).replace(" ", "") == string.replace(" ", "")
    except:
        value, success = failed_interpretation
    if success:
        return value, True

    try:
        value = asgt.literal_eval(string)
        success = type(value) is expected_type
        if not success:
            value = None
    except (SyntaxError, ValueError):
        value, success = failed_interpretation

    return value, success


def AsComplexInterpretedObject(
    string: str,
    /,
    *,
    expected_type: raw_hint_h | hint_node_t | None = None,
) -> tuple[Any, bool]:
    """"""
    if isinstance(expected_type, (GenericAlias, UnionType, hint_node_t)):
        value, _ = AsInterpretedObject(string)
        value_tree = _ValueTreeOfValue(value)
        if isinstance(expected_type, hint_node_t):
            hint_tree = expected_type
        else:
            hint_tree = HintTreeFromTypeHint(expected_type)
        if _CastValueTree(value_tree, hint_tree):
            return _ValueFromValueTree(value_tree), True
        else:
            return None, False

    return AsInterpretedObject(string, expected_type=expected_type)


def _ValueTreeOfValue(value: Any, /) -> _value_node_t:
    """"""
    if isinstance(value, Iterable) and not isinstance(value, str):
        elements = tuple(_ValueTreeOfValue(_elm) for _elm in value)
        return _value_node_t(consolidated=value, elements=elements)

    return _value_node_t(consolidated=value)


def _ValueFromValueTree(value_tree: _value_node_t, /) -> Any:
    """"""
    if isinstance(value_tree.consolidated, Iterable) and not isinstance(
        value_tree.consolidated, str
    ):
        elements = (_ValueFromValueTree(_elm) for _elm in value_tree.elements)
        return value_tree.type(elements)

    return value_tree.type(value_tree.consolidated)


def _CastValueTree(value_node: _value_node_t, hint_node: hint_node_t, /) -> bool:
    """"""
    if hint_node.type is None:  # Or
        if any(_CastValueTree(value_node, _elm) for _elm in hint_node.elements):
            return True
        else:
            return False

    if not isinstance(value_node.consolidated, hint_node.type):
        try:
            _ = hint_node.type(value_node.consolidated)
            success = True
        except:
            success = False
        if not success:
            return False
    if hint_node.elements is None:
        value_node.type = hint_node.type
        return True

    n_value_children = value_node.elements.__len__()
    n_hint_elements = hint_node.elements.__len__()
    has_ellipsis = (n_hint_elements == 2) and (hint_node.elements[1].type is Ellipsis)
    should_fake_ellipsis = (n_hint_elements == 1) and issubclass(
        hint_node.type, (list, set)
    )
    if has_ellipsis or should_fake_ellipsis or (n_value_children == n_hint_elements):
        if has_ellipsis or should_fake_ellipsis:
            hint_elements = n_value_children * (hint_node.elements[0],)
        else:
            hint_elements = hint_node.elements
        for value_elm, hint_elm in zip(value_node.elements, hint_elements):
            if not _CastValueTree(value_elm, hint_elm):
                return False
        value_node.type = hint_node.type
        return True

    return False

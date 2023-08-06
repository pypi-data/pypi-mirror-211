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

import dataclasses as dtcl
from typing import Any, Sequence

from conf_ini_g.instance.parameter.base import Pieces, base_t
from conf_ini_g.specification.parameter.type import type_options_t, type_t
from conf_ini_g.specification.parameter.value import INVALID_VALUE
from conf_ini_g.standard.path_extension import path_t


@dtcl.dataclass(repr=False, eq=False)
class unit_instance_t(base_t):
    def SetValue(
        self,
        value_w_comment: str | Any,
        comment_marker: str,
        type_options: type_options_t | None,
        /,
        *,
        __: str = None,
    ) -> None:
        """
        value_w_unit_w_comment: can be an uninterpreted string coming from an INI
        document, or can be an interpreted value coming from an interface.
        """
        if isinstance(value_w_comment, str):
            value_as_str, comment = _ValueAndComment(value_w_comment, comment_marker)
        else:
            value_as_str, comment = value_w_comment, None

        value, value_type = type_options.TypedValueAndType(value_as_str)
        if isinstance(value, str):
            # number_as_str_t will leave an str-typed value as is. Hence, it must be
            # converted here. But the call to type_options.TypedValueAndType allows to
            # benefit from type checking.
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
                value_type = type_t.NewFromType(type(value))
            except ValueError:
                value = INVALID_VALUE
                value_type = None

        self.type = value_type
        self.value = value
        self.comment = comment

    def FinalValue(self, _=None) -> tuple[Any, list[str]]:
        """"""
        if (value := self.value) is INVALID_VALUE:
            return INVALID_VALUE, ["Invalid value."]

        return value, []

    def Text(self) -> str:
        """"""
        return str(self.value)


def ConvertedValue(
    value: Any, conversion_factor: int | float, /
) -> tuple[Any, list[str]]:
    """"""
    unconverted_values = []

    if _ValueIsNotUnitCompatible(value):
        converted = value
    elif isinstance(value, (int, float)):
        converted = conversion_factor * value
    elif isinstance(value, Sequence):
        converted = []
        for element in value:
            converted_elm, unconverted_elm = ConvertedValue(element, conversion_factor)
            converted.append(converted_elm)
            unconverted_values.extend(unconverted_elm)
        converted = tuple(converted)
    else:
        converted = value
        unconverted_values.append(str(value))

    return converted, unconverted_values


def _ValueAndComment(
    value_w_comment: str,
    comment_marker: str,
    /,
) -> tuple[str, str | None]:
    """"""
    value_as_str, comment = Pieces(value_w_comment, comment_marker)
    if (comment is not None) and (comment.__len__() == 0):
        comment = None

    return value_as_str, comment


def _ValueIsNotUnitCompatible(value: Any, /) -> bool:
    """"""
    return (
        (value is None)
        or isinstance(value, bool)
        or isinstance(value, str)
        or isinstance(value, path_t)
    )

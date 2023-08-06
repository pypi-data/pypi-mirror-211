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
from typing import Any

from conf_ini_g.instance.parameter.base import Pieces, base_t
from conf_ini_g.instance.parameter.unit import ConvertedValue
from conf_ini_g.specification.parameter.main import parameter_t
from conf_ini_g.specification.parameter.type import type_options_t, type_t
from conf_ini_g.specification.parameter.unit import UNIT_SEPARATOR
from conf_ini_g.specification.parameter.value import (
    INVALID_VALUE,
    MISSING_REQUIRED_VALUE,
    invalid_value_t,
)


@dtcl.dataclass(repr=False, eq=False)
class instance_t(base_t):
    unit: str = None

    def SetDefaultValue(self, parameter: parameter_t, /) -> None:
        """"""
        value = parameter.default
        if value is MISSING_REQUIRED_VALUE:
            default_type = None
        else:
            default_type = parameter.types.MatchingTypeOf(value)

        self.type = default_type
        self.value = value

    def SetValue(
        self,
        value_w_unit_w_comment: str | Any,
        comment_marker: str,
        type_options: type_options_t | None,
        /,
        *,
        unit: str = None,
    ) -> None:
        """
        value_w_unit_w_comment: can be an uninterpreted string coming from an INI
        document, or can be an interpreted value coming from an interface.
        """
        if isinstance(value_w_unit_w_comment, str):
            value_as_str, inline_unit, comment = _ValueUnitAndComment(
                value_w_unit_w_comment, comment_marker
            )
            if unit is None:
                unit = inline_unit
        else:
            value_as_str, comment = value_w_unit_w_comment, None

        if type_options is None:
            value = value_as_str
            value_type = type_t.NewFromType(type(value))
        else:
            value, value_type = type_options.TypedValueAndType(value_as_str)
        # Do not consume unit here. It would be "redundant" with its storage in the
        # "unit" field. Instead, this will be handled by instance.config_t.AsRawConfig.

        self.type = value_type
        self.value = value
        self.unit = unit
        self.comment = comment

    def FinalValue(
        self, unit_conversions: dict[str, int | float | invalid_value_t] = None
    ) -> tuple[Any, list[str]]:
        """
        Final=with unit consumed.
        """
        if (value := self.value) is INVALID_VALUE:
            return INVALID_VALUE, ["Invalid value."]

        if (unit := self.unit) is None:
            return value, []

        conversion_factor = unit_conversions[unit]
        if conversion_factor is INVALID_VALUE:
            return INVALID_VALUE, ["Invalid unit value."]

        converted, unconverted = ConvertedValue(value, conversion_factor)
        if unconverted.__len__() > 0:
            unconverted = ", ".join(unconverted)
            return INVALID_VALUE, [
                f"{unconverted}: Value(s) do(es) not support unit conversion."
            ]

        return converted, []

    def Text(self) -> str:
        """"""
        text = str(self.value)

        if self.unit is None:
            return text

        return f"{text}{UNIT_SEPARATOR}{self.unit}"


def _ValueUnitAndComment(
    value_w_unit_w_comment: str,
    comment_marker: str,
    /,
) -> tuple[str, str | None, str | None]:
    """"""
    value_w_unit, comment = Pieces(value_w_unit_w_comment, comment_marker)
    if (comment is not None) and (comment.__len__() == 0):
        comment = None

    value_as_str, unit = Pieces(value_w_unit, UNIT_SEPARATOR, from_left=False)
    # if unit.__len__() == 0, do not make it None so that an invalid unit error is noticed later on

    return value_as_str, unit, comment

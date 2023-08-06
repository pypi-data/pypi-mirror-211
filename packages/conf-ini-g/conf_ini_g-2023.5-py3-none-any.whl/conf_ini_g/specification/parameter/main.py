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

import dataclasses as dtcl
import textwrap as text
from typing import Any, Sequence

from conf_ini_g.specification.base import base_t
from conf_ini_g.specification.parameter.type import type_options_t
from conf_ini_g.specification.parameter.value import (
    MISSING_REQUIRED_VALUE,
    missing_required_value_t,
)
from conf_ini_g.standard.str_extension import AlignedOnSeparator
from conf_ini_g.standard.type_extension import (
    NameValueTypeAsRichStr,
    TypeAsRichStr,
    any_hint_h,
)


@dtcl.dataclass(repr=False, eq=False)
class parameter_t(base_t):
    """
    types:
        At instantiation time: any_hint_h | Sequence[any_hint_h].
        After __post_init__: type_options_t
    default:
        Can be None only if types contains None at instantiation time
    """

    types: any_hint_h | Sequence[any_hint_h] | type_options_t = None
    default: Any = MISSING_REQUIRED_VALUE

    def __post_init__(self) -> None:
        """"""
        if self.types is None:
            return

        if isinstance(self.types, Sequence):
            types = self.types
        else:
            types = (self.types,)

        self.types = type_options_t.NewFromTypes(types)

    def Issues(self) -> list[str]:
        """"""
        output = super().Issues()

        if self.optional:
            output.extend(f"[{self.name}] {_iss}" for _iss in self.types.Issues())
            if self.default is MISSING_REQUIRED_VALUE:
                output.append(
                    f"{self.name}: Default value of optional parameter cannot be of type "
                    f'"{missing_required_value_t.__name__}"'
                )
            elif not self.types.ValueIsCompliant(self.default):
                output.append(
                    f'{self.default}: Invalid default value of parameter "{self.name}""'
                )
        else:
            if not self.basic:
                output.append(f"{self.name}: Parameter is not basic but not optional")
            if self.default is not MISSING_REQUIRED_VALUE:
                output.append(
                    f"{self.name}: Default value of mandatory parameter must be of type "
                    f'"{missing_required_value_t.__name__}"'
                )

        return output

    @property
    def optional(self) -> bool:
        """"""
        return self.default is not MISSING_REQUIRED_VALUE

    def __rich__(self) -> str:
        """"""
        output = [
            TypeAsRichStr(self),
            *text.indent(super().__rich__(), "    ").splitlines(),
            f"    [blue]Types[/]@=@{self.types.__rich__()}",
            f"    {NameValueTypeAsRichStr('Default', self.default, separator='@=@')}",
            f"    [blue]Optional[/]@=@{self.optional}",
        ]

        output = AlignedOnSeparator(output, "@=@", " = ")

        return "\n".join(output)

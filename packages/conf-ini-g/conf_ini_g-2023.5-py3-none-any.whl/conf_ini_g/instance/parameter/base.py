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
from abc import ABC as abstract_class_t
from abc import abstractmethod
from typing import Any

from rich.text import Text as text_t

from conf_ini_g.specification.parameter.type import type_options_t, type_t
from conf_ini_g.specification.parameter.value import INVALID_VALUE


@dtcl.dataclass(repr=False, eq=False)
class base_t(abstract_class_t):
    type: type_t = None
    value: Any = None
    comment: str = None

    @abstractmethod
    def SetValue(
        self,
        value_w_unit_w_comment: str | Any,
        comment_marker: str,
        type_options: type_options_t | None,
        /,
        *,
        unit: str = None,
    ) -> None:
        """"""
        ...

    @abstractmethod
    def Text(self) -> str:
        """"""
        ...

    def Issues(self) -> list[str]:
        """"""
        if self.value is INVALID_VALUE:
            return [f"No matching type in specification or invalid value"]

        return []

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        if self.type is None:
            return f"[blue]{type(self).__name__}[/]={self.Text()}"

        return (
            f"[blue]{type(self).__name__}[/]={self.Text()}"
            f"[yellow]:{self.type.py_type.__name__}[/]"
        )


def Pieces(
    combined: str, separator: str, /, *, from_left: bool = True
) -> tuple[str, str | None]:
    """"""
    if from_left:
        where_separator = combined.find(separator)
    else:
        where_separator = combined.rfind(separator)

    if where_separator != -1:
        left = combined[:where_separator].strip()
        right = combined[(where_separator + 1) :].strip()
    else:
        left = combined
        right = None

    return left, right

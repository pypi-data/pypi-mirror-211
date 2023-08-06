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
from typing import Annotated, Any, ClassVar

from conf_ini_g.specification.parameter.annotation import (
    annotation_t,
    py_type_options_h,
)
from conf_ini_g.standard.type_extension import annotated_hint_t


@dtcl.dataclass(repr=False, eq=False)
class sequence_t(annotation_t):
    VALID_PY_TYPES: ClassVar[py_type_options_h] = tuple
    ANY_LENGTH: ClassVar[tuple[int]] = (0,)

    # Any=Value of any type but None
    items_types: type | tuple[type | None, ...] = (None, Any)
    lengths: tuple[int, ...] = ANY_LENGTH

    def __post_init__(self):
        """"""
        # TODO: Convert every type to annotated type (works with Any b.t.w), maybe.
        #     However, there currently is a problem of circular import.
        if (self.items_types is Any) or isinstance(self.items_types, type):
            self.items_types = (self.items_types,)
        if isinstance(self.lengths, int):
            self.lengths = (self.lengths,)
        else:
            self.lengths = tuple(sorted(self.lengths))

    @classmethod
    def NewAnnotatedType(
        cls,
        items_types: type | tuple[type | None, ...] = (None, Any),
        lengths: tuple[int, ...] = ANY_LENGTH,
    ) -> annotated_hint_t:
        """"""
        return Annotated[
            cls.VALID_PY_TYPES, cls(items_types=items_types, lengths=lengths)
        ]

    def Issues(self, py_type: type, /) -> list[str]:
        """"""
        output = super().Issues(py_type)

        self_class = self.__class__
        if all(_typ is None for _typ in self.items_types):
            output.append(f'{self}: Contents types restricted to "None" for parameter')

        for content_type in self.items_types:
            if not (
                (content_type is None)
                or (content_type is Any)
                or isinstance(content_type, type)
            ):
                output.append(
                    f"{content_type}: Invalid item type in {self}; Expected=None, typing.Any, Python types"
                )
        if self.lengths != self_class.ANY_LENGTH:
            for length in self.lengths:
                if (not isinstance(length, int)) or (length <= 0):
                    output.append(
                        f"{length}: Invalid sequence length in {self}; Expected=strictly positive integer"
                    )

        return output

    def ValueIsCompliant(self, value: tuple, /) -> bool:
        """"""
        if (self.lengths != self.__class__.ANY_LENGTH) and (
            value.__len__() not in self.lengths
        ):
            return False

        none_not_allowed = None not in self.items_types
        any_not_present = Any not in self.items_types
        # If empty, isinstance(element, types_wo_none) returns False; But cannot be empty (see Issues).
        types_wo_none = tuple(_typ for _typ in self.items_types if _typ is not None)
        for element in value:
            if element is None:
                if none_not_allowed:
                    return False
            elif any_not_present and not isinstance(element, types_wo_none):
                return False

        return True

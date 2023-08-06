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
from types import EllipsisType, GenericAlias, UnionType
from typing import Annotated, Any, Sequence, get_args, get_origin

from conf_ini_g.standard.py_extension import SpecificationPath


raw_hint_h = type | GenericAlias | UnionType
annotated_hint_t = type(Annotated[object, None])
any_hint_h = raw_hint_h | annotated_hint_t

none_t = type(None)  # is NoneType, but Mypy complains otherwise.


FAKE_TYPE_ANNOTATION = None
UNIVERSAL_ANNOTATED_TYPE = Annotated[raw_hint_h, FAKE_TYPE_ANNOTATION]
UNIVERSAL_ANNOTATED_TYPES = (None, UNIVERSAL_ANNOTATED_TYPE)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class hint_node_t:
    type: type | EllipsisType | None  # None=OR
    elements: tuple[hint_node_t, ...] | None = None


def HintTreeFromTypeHint(type_hint: raw_hint_h | EllipsisType, /) -> hint_node_t:
    """"""
    if (origin := get_origin(type_hint)) is None:
        return hint_node_t(type=type_hint)

    # Handled types: list, set, tuple, with sets using the dict delimiters { and }.
    if origin is dict:
        raise TypeError(f"{origin.__name__}: Unhandled type.")

    elements = tuple(HintTreeFromTypeHint(_elm) for _elm in get_args(type_hint))

    if origin is UnionType:
        return hint_node_t(type=None, elements=elements)

    return hint_node_t(type=origin, elements=elements)


def PythonTypeOfAnnotated(annotated_hint: annotated_hint_t, /) -> type:
    """"""
    return annotated_hint.__args__[0]


def AnnotationsOfType(annotated_hint: annotated_hint_t, /) -> Sequence[Any]:
    """"""
    return tuple(
        _nnt for _nnt in annotated_hint.__metadata__ if _nnt is not FAKE_TYPE_ANNOTATION
    )


def TypeAsRichStr(instance: Any, /, *, relative_to_home: bool = True) -> str:
    """"""
    return (
        f"[bold magenta]{type(instance).__name__}[/]"
        f"[gray]@"
        f"{SpecificationPath(type(instance), relative_to_home=relative_to_home)}:[/]"
    )


def NameValueTypeAsRichStr(name: str, value: Any, /, *, separator: str = "=") -> str:
    """"""
    if isinstance(value, Sequence) and (value.__len__() == 0):
        value = "[cyan]<empty>[/]"

    return f"[blue]{name}[/]{separator}{value}[yellow]:{type(value).__name__}[/]"

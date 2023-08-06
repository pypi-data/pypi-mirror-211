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
from typing import Annotated, Any, Sequence

from rich.text import Text as text_t

from conf_ini_g.catalog.specification.parameter.boolean import boolean_t
from conf_ini_g.catalog.specification.parameter.choices import choices_t
from conf_ini_g.catalog.specification.parameter.number import number_t
from conf_ini_g.catalog.specification.parameter.path import path_t
from conf_ini_g.catalog.specification.parameter.sequence import sequence_t
from conf_ini_g.specification.parameter.annotation import annotation_t
from conf_ini_g.specification.parameter.value import INVALID_VALUE
from conf_ini_g.standard.path_extension import path_t as pl_path_t
from conf_ini_g.standard.str_extension import AsInterpretedObject
from conf_ini_g.standard.type_extension import (
    FAKE_TYPE_ANNOTATION,
    AnnotationsOfType,
    PythonTypeOfAnnotated,
    annotated_hint_t,
    any_hint_h,
    none_t,
)


@dtcl.dataclass(repr=False, eq=False)
class type_t:
    py_type: type = None
    annotations: Sequence[annotation_t] = None

    @classmethod
    def NewFromType(cls, type_: any_hint_h | None, /) -> type_t:
        """
        type_: Can be None if None is accepted as a value for a parameter.
        """
        if isinstance(type_, (type, none_t)):
            type_ = Annotated[type_, FAKE_TYPE_ANNOTATION]

        return cls.NewFromAnnotatedType(type_)

    @classmethod
    def NewFromAnnotatedType(cls, annotated_type: annotated_hint_t, /) -> type_t:
        """"""
        output = cls()

        output.py_type = PythonTypeOfAnnotated(annotated_type)
        output.annotations = AnnotationsOfType(annotated_type)

        return output

    def Issues(self) -> list[str]:
        """"""
        output = []

        py_type = self.py_type
        for annotation in self.annotations:
            output.extend(f"[{self}] {_iss}" for _iss in annotation.Issues(py_type))

        return output

    def ContainsOrMatches(
        self,
        expected_annotation: annotation_t | Sequence[annotation_t],
        /,
        *,
        py_type: type = None,
        full: bool = False,
    ) -> bool:
        """"""
        if (py_type is not None) and (self.py_type is not py_type):
            return False

        ref_types = tuple(type(_nnt) for _nnt in self.annotations)
        if isinstance(expected_annotation, Sequence):
            expected_annotations = expected_annotation
        else:
            expected_annotations = (expected_annotation,)

        if full:
            # Comparing the iterators returns False, hence the conversions to lists
            # (through sorted, which is necessary).
            type_name = lambda _elm: _elm.__name__
            ref_types = sorted(ref_types, key=type_name)
            expected_types = sorted(
                (type(_nnt) for _nnt in expected_annotations), key=type_name
            )

            return ref_types == expected_types
        else:
            n_founds = 0
            for annotation in expected_annotations:
                if isinstance(annotation, ref_types):
                    n_founds += 1

            return n_founds == expected_annotations.__len__()

    def FirstAnnotationWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> annotation_t | None:
        """"""
        # Do not test isinstance(attribute, Sequence) since str is a sequence
        if isinstance(attribute, str):
            attributes = (attribute,)
        else:
            attributes = attribute

        for annotation in self.annotations:
            if all(hasattr(annotation, _ttr) for _ttr in attributes):
                return annotation

        return None

    def ValueIsCompliant(self, value: Any, /) -> bool:
        """"""
        return isinstance(value, self.py_type) and all(
            _nnt.ValueIsCompliant(value) for _nnt in self.annotations
        )

    def TypedValue(self, value: Any, /) -> tuple[Any | None, bool]:
        """"""
        if isinstance(value, self.py_type):
            return value, True

        if isinstance(value, str):
            typed_value, success = AsInterpretedObject(
                value, expected_type=self.py_type
            )
            if success and self.ValueIsCompliant(typed_value):
                return typed_value, True

        return INVALID_VALUE, False

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        if self.py_type is none_t:
            type_name = "None"
        else:
            type_name = self.py_type.__name__
        output = [f"[blue]{type_name}[/]"]

        for annotation in self.annotations:
            output.append(type(annotation).__name__)

        return "&".join(output)


@dtcl.dataclass(init=False, repr=False, eq=False)
class type_options_t(list[type_t]):
    """"""

    @classmethod
    def NewFromTypes(cls, any_types: Sequence[any_hint_h | None], /) -> type_options_t:
        """"""
        output = cls()

        idx_o_none = 0
        for t_idx, any_type in enumerate(any_types):
            type_ = type_t.NewFromType(any_type)
            output.append(type_)
            if type_.py_type is none_t:
                idx_o_none = t_idx

        if idx_o_none > 0:
            keep = output[idx_o_none]
            del output[idx_o_none]
            output.insert(0, keep)

        return output

    @property
    def n_types(self) -> int:
        """"""
        return self.__len__()

    def Issues(self) -> list[str]:
        """"""
        output = []

        if self.n_types == 0:
            output.append(f"{self}: Empty list of allowed types")
        else:
            if (self.n_types == 1) and self.AllowsNone():
                output.append(f"{self}: None cannot be the only allowed type")
            n_nones = 0
            for cstd_type in self:
                if cstd_type.py_type is none_t:
                    n_nones += 1
                else:
                    output.extend(f"[{self}] {_iss}" for _iss in cstd_type.Issues())
            if n_nones > 1:
                output.append(f"{self}: None cannot be mentioned more than once")

        return output

    def AllowsNone(self) -> bool:
        """"""
        return self[0].py_type is none_t

    def MatchingTypeOf(self, value: Any, /) -> type_t:
        """"""
        output = None

        for cstd_type in self:
            if isinstance(value, cstd_type.py_type):
                output = cstd_type
                break

        return output

    def ValueIsCompliant(self, value: Any, /) -> bool:
        """"""
        return any(_tpe.ValueIsCompliant(value) for _tpe in self)

    def TypedValueAndType(self, value: str, /) -> tuple[Any, type_t | None]:
        """"""
        typed_value = INVALID_VALUE
        type_spec = None

        for type_ in self:
            typed_value, success = type_.TypedValue(value)
            if success:
                type_spec = type_
                break

        return typed_value, type_spec

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = (_typ.__rich__() for _typ in self)

        return " + ".join(output)


BASIC_TYPES: dict[str, type_t] = {
    "boolean": type_t.NewFromAnnotatedType(Annotated[bool, boolean_t()]),
    "float": type_t.NewFromAnnotatedType(Annotated[float, number_t()]),
    "int": type_t.NewFromAnnotatedType(Annotated[int, number_t()]),
    "choices": type_t.NewFromAnnotatedType(Annotated[str, choices_t()]),
    "path": type_t.NewFromAnnotatedType(
        Annotated[pl_path_t, path_t(target_type=path_t.TARGET_TYPE.any, is_input=True)]
    ),
    "sequence": type_t.NewFromAnnotatedType(Annotated[tuple, sequence_t()]),
    "None": type_t.NewFromAnnotatedType(Annotated[None, FAKE_TYPE_ANNOTATION]),
}

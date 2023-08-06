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
from typing import Any, Type

from conf_ini_g.catalog.interface.screen.library.pyqt5.constant import (
    SIZE_EXPANDING,
    SIZE_FIXED,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.main import (
    label_wgt_t,
    library_wgt_t,
    stack_wgt_t,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.text import text_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.boolean import boolean_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.choices import choices_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.none import none_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.path import path_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.sequence import sequence_wgt_t
from conf_ini_g.catalog.interface.screen.parameter.text import default_entry_wgt_t
from conf_ini_g.instance.parameter.main import instance_t
from conf_ini_g.interface.screen.generic import FormattedName
from conf_ini_g.interface.screen.parameter.type_selector import type_selector_wgt_t
from conf_ini_g.specification.parameter.main import parameter_t as parameter_spec_t
from conf_ini_g.specification.parameter.type import BASIC_TYPES, type_t
from conf_ini_g.specification.parameter.unit import UNIT_SEPARATOR
from conf_ini_g.standard.type_extension import any_hint_h

_TYPE_WIDGET_TRANSLATOR: dict[type_t, Type[library_wgt_t]] = {
    BASIC_TYPES["boolean"]: boolean_wgt_t,
    BASIC_TYPES["float"]: default_entry_wgt_t,
    BASIC_TYPES["int"]: default_entry_wgt_t,
    BASIC_TYPES["choices"]: choices_wgt_t,
    BASIC_TYPES["path"]: path_wgt_t,
    BASIC_TYPES["sequence"]: sequence_wgt_t,
    BASIC_TYPES["None"]: none_wgt_t,
}


@dtcl.dataclass(repr=False, eq=False)
class parameter_t:
    """
    In order to leave the section widget put the name, type, and input widgets of each parameter in columns,
    parameter_t is not a container widget. Instead, it just stores its component widgets for later addition to a layout.
    """

    name: label_wgt_t = None
    type_selector: label_wgt_t | type_selector_wgt_t = None
    value_stack: stack_wgt_t = None
    unit: text_wgt_t = None
    comment: str = None

    @classmethod
    def NewForParameter(
        cls, parameter_spec: parameter_spec_t, instance: instance_t, /
    ) -> parameter_t:
        """"""
        output = cls()

        formatted_name = FormattedName(parameter_spec.name, " ")

        comment = f"{formatted_name}\n{parameter_spec.definition}.\n\n{parameter_spec.description}."
        if instance.comment is not None:
            comment += f"\n\n{instance.comment}."
        output.comment = comment

        output.name = label_wgt_t(formatted_name)
        output.name.setToolTip(comment)

        types = parameter_spec.types
        if types is None:
            type_selector = label_wgt_t("Unspecified")
            types = (instance.type,)
        elif types.__len__() > 1:
            type_selector = type_selector_wgt_t(types, instance.type)
        else:
            type_selector = label_wgt_t(types[0].py_type.__name__)
        output.type_selector = type_selector

        value_stack = stack_wgt_t()
        initial_index = 0
        for t_idx, value_type in enumerate(types):
            if value_type is instance.type:
                initial_value = instance.value
                initial_index = t_idx
            else:
                initial_value = None
            widget_type = _WidgetTypeForType(value_type)
            value = widget_type.NewWithDetails(
                initial_value,
                value_type,
                parameter_spec,
            )
            value_stack.addWidget(value)
        value_stack.setCurrentIndex(initial_index)
        value_stack.setSizePolicy(SIZE_EXPANDING, SIZE_FIXED)
        output.value_stack = value_stack

        if (unit := getattr(instance, "unit", None)) is not None:
            output.unit = text_wgt_t(unit)

        name_style = "padding-right: 5px;"
        if parameter_spec.optional:
            name_style += "color: gray;"
        output.name.setStyleSheet(name_style)
        output.type_selector.setStyleSheet(name_style)

        if isinstance(type_selector, type_selector_wgt_t):
            type_selector.SetFunction(output.value_stack.setCurrentIndex)

        return output

    def SetVisible(self, visible: bool, /) -> None:
        """"""
        self.name.setVisible(visible)
        self.type_selector.setVisible(visible)
        self.value_stack.setVisible(visible)
        if self.unit is not None:
            self.unit.setVisible(visible)

    @property
    def active_value(self) -> library_wgt_t:
        """"""
        return self.value_stack.currentWidget()

    def Value(self) -> Any:
        """"""
        return self.active_value.Value()

    def Text(self) -> str:
        """"""
        text = self.active_value.Text()

        if self.unit is None:
            return text

        return f"{text}{UNIT_SEPARATOR}{self.unit.Text()}"


def RegisterNewTranslation(
    new_type: any_hint_h, widget_type: Type[library_wgt_t], /
) -> None:
    """"""
    value_type = type_t.NewFromType(new_type)
    if value_type in _TYPE_WIDGET_TRANSLATOR:
        # Raising an exception is adapted here since it is a developer-oriented function
        raise ValueError(
            f'{value_type}: Type already registered with "{_TYPE_WIDGET_TRANSLATOR[value_type]}" '
            f"in type-to-widget translations."
        )

    _TYPE_WIDGET_TRANSLATOR[value_type] = widget_type


def _WidgetTypeForType(value_type: type_t, /) -> Type[library_wgt_t]:
    """"""
    for registered_type, widget_type in _TYPE_WIDGET_TRANSLATOR.items():
        if value_type.ContainsOrMatches(
            registered_type.annotations, py_type=registered_type.py_type
        ):
            return widget_type

    return default_entry_wgt_t

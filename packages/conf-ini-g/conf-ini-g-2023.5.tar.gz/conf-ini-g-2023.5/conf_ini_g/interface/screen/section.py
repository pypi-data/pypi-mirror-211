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

from typing import ClassVar, Iterator, Sequence

from conf_ini_g.catalog.interface.screen.library.pyqt5.constant import (
    ALIGNED_RIGHT,
    ALIGNED_TOP,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.main import (
    grid_lyt_t,
    group_wgt_t,
    hbox_lyt_t,
    label_wgt_t,
    library_wgt_t,
    stack_wgt_t,
)
from conf_ini_g.instance.parameter.main import instance_t
from conf_ini_g.interface.screen.generic import FormattedName
from conf_ini_g.interface.screen.parameter.main import parameter_t
from conf_ini_g.specification.parameter.main import parameter_t as parameter_spec_t
from conf_ini_g.specification.section.main import controller_t
from conf_ini_g.specification.section.main import section_t as section_spec_t


class _base_t(group_wgt_t):  # Cannot be abstracted
    HEADER_NAMES: ClassVar[tuple[str]] = (
        "Parameter",
        "Type(s)",
        "Value",
        "Unit",
    )
    HEADER_STYLE: ClassVar[str] = "background-color: darkgray; padding-left: 5px;"

    formatted_name: str

    @classmethod
    def NewWithName(cls, name: str, /, *, controller: controller_t = None) -> _base_t:
        """"""
        output = cls()

        if controller is None:
            controller = ""
        else:
            controller = f" ⮜ {controller.section}.{controller.parameter}"
        output.formatted_name = FormattedName(name, " ") + controller

        output.setTitle(output.formatted_name)

        return output

    @classmethod
    def Headers(cls) -> Sequence[label_wgt_t]:
        """"""
        output = []

        for text in cls.HEADER_NAMES:
            header = label_wgt_t(f'<font color="blue">{text}</font>')
            header.setStyleSheet(cls.HEADER_STYLE)
            output.append(header)

        return output

    @property
    def all_parameters(self) -> Sequence[dict[str, parameter_t]]:
        """"""
        raise NotImplementedError

    @property
    def active_parameters(self) -> dict[str, parameter_t]:
        """"""
        raise NotImplementedError

    def __contains__(self, key: str, /) -> bool:
        """"""
        return any(key in _set.keys() for _set in self.all_parameters)

    def __getitem__(self, key: str, /) -> parameter_t:
        """"""
        for parameter_set in self.all_parameters:
            if key in parameter_set:
                return parameter_set[key]

        raise KeyError(f"{key}: Not a parameter of section {self.formatted_name}.")

    def __iter__(self) -> Iterator[parameter_t]:
        """"""
        for parameter_set in self.all_parameters:
            for parameter in parameter_set:
                yield parameter


class section_t(_base_t):
    __slots__ = ("parameters",)
    parameters: dict[str, parameter_t]

    @classmethod
    def NewForSection(
        cls, section_spec: section_spec_t, instances: dict[str, instance_t], /
    ) -> section_t | None:
        """"""
        output = cls.NewWithName(section_spec.name)

        parameters, parameter_names, layout = _ParametersFromSpecifications(
            section_spec, instances
        )
        if parameters.__len__() == 0:
            return None

        output.parameters = dict(zip(parameter_names, parameters))

        for h_idx, header in enumerate(cls.Headers()):
            layout.addWidget(header, 0, h_idx)
        output.setLayout(layout)

        return output

    @property
    def all_parameters(self) -> Sequence[dict[str, parameter_t]]:
        """"""
        return (self.parameters,)

    @property
    def active_parameters(self) -> dict[str, parameter_t]:
        """"""
        return self.parameters


class controlled_section_t(_base_t):
    __slots__ = ("parameter_sets", "page_stack")
    parameter_sets: list[dict[str, parameter_t]]
    page_stack: stack_wgt_t

    @classmethod
    def NewForSection(
        cls,
        section_spec: section_spec_t,
        controller: controller_t,
        controller_value: str,
        instances: dict[str, instance_t],
        /,
    ) -> controlled_section_t | None:
        """"""
        output = cls.NewWithName(section_spec.name, controller=controller)

        parameter_sets = []
        page_stack = stack_wgt_t()
        for parameter_specs in (section_spec, *section_spec.alternatives.values()):
            parameters, parameter_names, layout = _ParametersFromSpecifications(
                parameter_specs, instances
            )
            if parameters.__len__() == 0:
                continue

            parameter_sets.append(dict(zip(parameter_names, parameters)))

            for h_idx, header in enumerate(cls.Headers()):
                layout.addWidget(header, 0, h_idx)
            page = library_wgt_t()
            page.setLayout(layout)
            page_stack.addWidget(page)

        if parameter_sets.__len__() == 0:
            return None

        output.parameter_sets = parameter_sets
        output.page_stack = page_stack

        controlling_values = section_spec.controlling_values
        page_stack.setCurrentIndex(controlling_values.index(controller_value))

        # Curiously, the stacked widget cannot be simply declared as child of instance;
        # This must be specified through a layout.
        layout = hbox_lyt_t()
        layout.addWidget(page_stack)
        layout.setContentsMargins(0, 0, 0, 0)
        output.setLayout(layout)

        return output

    @property
    def all_parameters(self) -> Sequence[dict[str, parameter_t]]:
        """"""
        return self.parameter_sets

    @property
    def active_parameters(self) -> dict[str, parameter_t]:
        """"""
        return self.parameter_sets[self.page_stack.currentIndex()]


def _ParametersFromSpecifications(
    specifications: section_spec_t | Iterator[parameter_spec_t],
    instances: dict[str, instance_t],
    /,
) -> tuple[Sequence[parameter_t], Sequence[str], grid_lyt_t]:
    """"""
    parameters = []
    parameter_names = []

    layout = grid_lyt_t()
    layout.setAlignment(ALIGNED_TOP)
    layout.setColumnStretch(0, 4)
    layout.setColumnStretch(1, 4)
    layout.setColumnStretch(2, 8)
    layout.setColumnStretch(3, 1)
    layout.setContentsMargins(0, 0, 0, 0)

    for row, parameter_spec in enumerate(specifications, start=1):
        parameter = parameter_t.NewForParameter(
            parameter_spec, instances[parameter_spec.name]
        )
        parameters.append(parameter)
        parameter_names.append(parameter_spec.name)

        layout.addWidget(parameter.name, row, 0, alignment=ALIGNED_RIGHT)
        layout.addWidget(parameter.type_selector, row, 1)
        layout.addWidget(parameter.value_stack, row, 2, 1, 2 - 1)
        if parameter.unit is not None:
            layout.addWidget(parameter.unit, row, 3)

    return parameters, parameter_names, layout

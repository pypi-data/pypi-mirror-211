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

from typing import Annotated, Callable, Iterator

from conf_ini_g.catalog.interface.screen.library.pyqt5.constant import ALIGNED_HCENTER
from conf_ini_g.catalog.interface.screen.library.pyqt5.main import (
    ShowErrorMessage,
    ShowMessage,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.button import button_wgt_t
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.main import (
    grid_lyt_t,
    hbox_lyt_t,
    label_wgt_t,
    library_wgt_t,
    tabs_wgt_t,
    vbox_lyt_t,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.scroll_container import (
    scroll_container_t,
)
from conf_ini_g.catalog.interface.screen.parameter.boolean import boolean_wgt_t
from conf_ini_g.catalog.specification.parameter.boolean import boolean_t
from conf_ini_g.catalog.specification.parameter.path import path_t
from conf_ini_g.instance.config import config_t as config_instance_t
from conf_ini_g.interface.screen.parameter.path_chooser import SelectedOutputFile
from conf_ini_g.interface.screen.section import controlled_section_t, section_t
from conf_ini_g.interface.storage.config import SaveRawConfigToINIDocument
from conf_ini_g.interface.storage.constant import INI_COMMENT_MARKER
from conf_ini_g.raw.config import AsStr, ini_config_h, raw_config_h
from conf_ini_g.specification.parameter.type import type_t
from conf_ini_g.standard.path_extension import path_t as pl_path_t


class config_t(library_wgt_t):
    __slots__ = (
        "instance",
        "sections",
    )
    # Widget might not cooperate well with list, in which case Python raises the
    # following exception: TypeError: multiple bases have instance lay-out conflict
    # To be safe, "sections" is field instead of being part of the class definition.
    sections: dict[str, section_t | controlled_section_t]
    instance: config_instance_t
    action_button: button_wgt_t
    Action: Callable[[raw_config_h], None]

    def __init__(self) -> None:
        """"""
        super().__init__()
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in config_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewFromConfig(
        cls,
        title: str | None,
        instance: config_instance_t,
        /,
        *,
        advanced_mode: bool = False,
        action: tuple[str, Callable[[raw_config_h], None]] = None,
    ) -> config_t:
        """"""
        output = cls()
        output.instance = instance
        output.Action = action[1]

        # --- Top-level widgets
        if title is None:
            components = []
        else:
            components = [title]
        home = pl_path_t.home()
        if instance.ini_path is not None:
            components.append(f"INI:{instance.ini_path.relative_to(home)}")
        components.append(f"SPEC:{instance.specification.spec_path}")
        title = "<br/>".join(components)

        title_wgt = label_wgt_t("<b>" + title + "</b>")
        title_wgt.setAlignment(ALIGNED_HCENTER)
        advanced_mode_lyt = _AdvancedModeLayout(advanced_mode, output)
        button_lyt = _ActionButtonsLayout(output, action, instance.ini_path is not None)

        # --- Sections
        categories = {}
        sections = {}
        controlled_sections = []

        for section_spec in instance.specification:
            if (controller := section_spec.controller) is None:
                section = section_t.NewForSection(
                    section_spec, instance[section_spec.name]
                )
            else:
                section = controlled_section_t.NewForSection(
                    section_spec,
                    controller,
                    instance.GetValueOfController(controller),
                    instance[section_spec.name],
                )
                if section is not None:
                    controlled_sections.append((section, section_spec))
            if section is None:
                continue

            sections[section_spec.name] = section

            if (category := section_spec.category) not in categories:
                contents = library_wgt_t(parent=None)
                scroll_area = scroll_container_t.NewForWidget(contents)
                layout = vbox_lyt_t()
                contents.setLayout(layout)
                categories[category] = (layout, scroll_area)

            layout = categories[category][0]
            layout.addWidget(section)

        output.sections = sections

        if categories.__len__() > 1:
            category_selector = tabs_wgt_t()
            for category, (_, scroll_area) in categories.items():
                category_selector.addTab(scroll_area, category)
        else:
            category = tuple(categories.keys())[0]
            category_selector = categories[category][1]

        for section, section_spec in controlled_sections:
            controller = section_spec.controller
            parameter = output[controller.section].parameters[controller.parameter]
            value_wgt = parameter.active_value
            if hasattr(value_wgt, "SetFunction"):
                value_wgt.SetFunction(section.page_stack.setCurrentIndex)
            else:
                ShowErrorMessage(
                    f'{controller.section}.{controller.parameter}: Controller has no "SetFunction" method; Disabling control'
                )

        # --- Layout...
        layout = grid_lyt_t()
        if title_wgt is None:
            first_available_row = 0
        else:
            layout.addWidget(title_wgt, 0, 0, 1, 1)
            first_available_row = 1
        layout.addWidget(category_selector, first_available_row, 0, 1, 1)
        layout.addLayout(advanced_mode_lyt, first_available_row + 1, 0, 1, 1)
        layout.addLayout(button_lyt, first_available_row + 2, 0, 1, 1)

        output.setLayout(layout)
        # --- ...Layout

        output.ToogleAdvancedMode(advanced_mode)

        return output

    def ToogleAdvancedMode(self, advanced_mode: bool, /) -> None:
        """"""
        for section_name, section in self.sections.items():
            section_spec = self.instance.specification[section_name]
            if section_spec.basic:
                should_check_parameters = True
            elif advanced_mode:
                section.setVisible(True)
                should_check_parameters = True
            else:
                section.setVisible(False)
                should_check_parameters = False

            if should_check_parameters:
                if (controller := section_spec.controller) is None:
                    parameter_specs = section_spec
                else:
                    controller_text = (
                        self[controller.section].parameters[controller.parameter].Text()
                    )
                    parameter_specs = section_spec.ActiveParameters(controller_text)
                for parameter, parameter_spec in zip(
                    section.active_parameters.values(), parameter_specs
                ):
                    if not parameter_spec.basic:
                        if advanced_mode:
                            parameter.setVisible(True)
                        else:
                            parameter.setVisible(False)

    def SynchronizeInstance(self) -> list[str]:
        """"""
        for section_name, section in self.sections.items():
            section_spec = self.instance.specification[section_name]
            if (controller := section_spec.controller) is None:
                parameter_specs = section_spec
            else:
                controller_text = (
                    self[controller.section].parameters[controller.parameter].Text()
                )
                parameter_specs = section_spec.ActiveParameters(controller_text)
            for parameter, parameter_spec in zip(
                section.active_parameters.values(), parameter_specs
            ):
                if parameter.unit is None:
                    unit_kwarg = {}
                else:
                    unit_kwarg = {"unit": parameter.unit.Text()}
                instance = self.instance[section_spec.name][parameter_spec.name]
                instance.SetValue(
                    parameter.Value(),
                    INI_COMMENT_MARKER,
                    parameter_spec.types,
                    **unit_kwarg,
                )

        return self.instance.Issues()

    def AsINIConfig(self) -> ini_config_h | None:
        """"""
        issues = self.SynchronizeInstance()
        if issues.__len__() == 0:
            output = self.instance.AsINIConfig()
        else:
            output = None
            ShowErrorMessage("\n".join(issues), parent=self)

        return output

    def ShowInINIFormat(self) -> None:
        """"""
        config = self.AsINIConfig()
        if config is None:
            return

        config = AsStr(config, in_html_format=True)
        ShowMessage("INI Config", "<tt>" + config + "<tt/>")

    def SaveConfig(self, new_ini: bool, /) -> None:
        """"""
        if new_ini:
            path = SelectedOutputFile(
                "Save Config As",
                "Save Config As",
                mode=path_t.TARGET_TYPE.document,
                valid_types={"Config files": ("ini", "INI")},
            )
        else:
            path = self.instance.ini_path  # Will overwrite current INI document

        if path is not None:
            config = self.AsINIConfig()
            error = SaveRawConfigToINIDocument(config, path)
            if error is None:
                self.instance.ini_path = path
            else:
                ShowErrorMessage(error, parent=self)

    def LaunchAction(self) -> None:
        """"""
        issues = self.SynchronizeInstance()
        if issues.__len__() == 0:
            raw_config, issues = self.instance.AsRawConfig()
            if issues.__len__() == 0:
                self.action_button.setEnabled(False)
                try:
                    self.Action(raw_config)
                except Exception as exception:
                    ShowErrorMessage(str(exception), parent=self)
                self.action_button.setEnabled(True)
            else:
                ShowErrorMessage("\n".join(issues), parent=self)
        else:
            ShowErrorMessage("\n".join(issues), parent=self)

    def __contains__(self, key: str, /) -> bool:
        """"""
        return key in self.sections

    def __getitem__(self, key: str, /) -> section_t | controlled_section_t:
        """"""
        return self.sections[key]

    def __iter__(self) -> Iterator[str]:
        """"""
        return self.sections.keys()


def _AdvancedModeLayout(advanced_mode: bool, config: config_t, /) -> hbox_lyt_t:
    """"""
    output = hbox_lyt_t()

    annotated_type = Annotated[bool, boolean_t(mode=boolean_t.MODE.on_off)]
    value_type = type_t.NewFromAnnotatedType(annotated_type)
    boolean = boolean_wgt_t.NewWithDetails(
        advanced_mode,
        value_type,
        None,
    )
    boolean.true_btn.SetFunction(config.ToogleAdvancedMode)

    output.addWidget(label_wgt_t("<i>Advanced Mode</i>"))
    output.addWidget(boolean)

    return output


def _ActionButtonsLayout(
    config: config_t,
    action: tuple[str, Callable[[raw_config_h], None]] | None,
    has_ini_document: bool,
    /,
) -> grid_lyt_t:
    """"""
    layout = grid_lyt_t()

    buttons = []
    geometries = []

    button = button_wgt_t("Show in INI format")
    button.SetFunction(config.ShowInINIFormat)
    buttons.append(button)
    geometries.append((0, 0, 1, 2))

    button = button_wgt_t("Save Config As")
    button.SetFunction(lambda: config.SaveConfig(True))
    buttons.append(button)
    if has_ini_document:
        geometries.append((1, 0, 1, 1))

        button = button_wgt_t("Save/Overwrite Config")
        button.SetFunction(lambda: config.SaveConfig(False))
        buttons.append(button)
        geometries.append((1, 1, 1, 1))
    else:
        geometries.append((1, 0, 1, 2))

    if action is None:
        label = "Close"
        Function = config.Close
    else:
        label = action[0]
        Function = config.LaunchAction

    button = button_wgt_t(label)
    button.SetFunction(Function)
    buttons.append(button)
    geometries.append((2, 0, 1, 2))

    config.action_button = button

    for button, geometry in zip(buttons, geometries):
        layout.addWidget(button, *geometry)
    layout.setContentsMargins(0, 0, 0, 0)

    return layout

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

from typing import ClassVar, Sequence

from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.choices import (
    choices_list_wgt_t,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.main import (
    hbox_lyt_t,
    library_wgt_t,
)
from conf_ini_g.catalog.interface.screen.library.pyqt5.widget.text import text_wgt_t
from conf_ini_g.catalog.specification.parameter.sequence import sequence_t
from conf_ini_g.specification.parameter.main import parameter_t
from conf_ini_g.specification.parameter.type import type_t
from conf_ini_g.specification.parameter.value import (
    MISSING_REQUIRED_VALUE,
    missing_required_value_t,
)


class sequence_wgt_t(library_wgt_t):
    ENTRY_ANY: ClassVar[str] = "any"
    ENTRIES: ClassVar[tuple[str, ...]] = ("2", "3", "4", "5", "6", ENTRY_ANY)

    __slots__ = ("length_selector", "components")
    length_selector: choices_list_wgt_t
    components: tuple[text_wgt_t, ...]

    def __init__(self, parent: library_wgt_t = None):
        """"""
        super().__init__(parent=parent)

        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in sequence_wgt_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewWithDetails(
        cls,
        value: tuple | None | missing_required_value_t,
        value_type: type_t,
        _: parameter_t,
    ) -> sequence_wgt_t:
        """
        If value_type does not contain the necessary details, a simple free-text input widget is used. If the value is not
        coherent with the details (which should not happen if value_type contains the necessary details and the value has
        been validated), a choice with the length of the value is added, with an exclamation point.
        """
        output = cls()

        if (value is None) or (value is MISSING_REQUIRED_VALUE):
            value = ()
        length = value.__len__()

        annotation = value_type.FirstAnnotationWithAttribute("lengths")
        if annotation is None:
            entries = cls.ENTRIES
            max_entry = int(entries[-2])
        elif (lengths := annotation.lengths) == sequence_t.ANY_LENGTH:
            entries = (cls.ENTRY_ANY,)
            max_entry = None
        else:
            entries = tuple(str(_lgh) for _lgh in lengths)
            max_entry = lengths[-1]
            if (length > 0) and (str(length) not in entries):
                # This should never happen since the value must have been validated
                entries = entries + (str(length) + "!",)
                max_entry = max(max_entry, length)

        if entries.__len__() > 1:
            length_selector = choices_list_wgt_t()
            for entry in entries:
                length_selector.addItem(entry)

            if (length_as_str := str(length)) in entries:
                length_selector.setCurrentText(length_as_str)
            if length_as_str + "!" in entries:
                length_selector.setCurrentText(length_as_str + "!")
            else:  # cls.ENTRY_ANY is necessarily in entries
                length_selector.setCurrentText(cls.ENTRY_ANY)

            output.length_selector = length_selector
            output.length_selector.SetFunction(output.SetLength)

        components = []
        if max_entry is None:
            value_as_str = str(value)[1:-1] if length > 0 else ""
            widget = text_wgt_t(value_as_str, parent=None)
            components.append(widget)
        else:
            for e_idx in range(max_entry):
                value_as_str = str(value[e_idx]) if e_idx < length else ""
                widget = text_wgt_t(value_as_str, parent=None)
                if e_idx >= length:
                    widget.setVisible(False)
                    widget.setEnabled(False)
                components.append(widget)
        output.components = tuple(components)

        layout = hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        if output.length_selector is not None:
            layout.addWidget(output.length_selector)
        for component in output.components:
            layout.addWidget(component)
        output.setLayout(layout)

        return output

    def SetLength(self, new_index: int) -> None:
        """"""
        new_length = self.length_selector.ItemAt(new_index)
        if new_length == self.__class__.ENTRY_ANY:
            new_length = 1
        elif new_length.endswith("!"):
            new_length = int(new_length[:-1])
        else:
            new_length = int(new_length)
        _AdjustComponents(self.components, new_length)

    def Text(self) -> str:
        """"""
        contents = []
        for component in self.components:
            # Do not use "visible" here since setting visible does not really set the property until it is actually
            # shown. The documentation explains about ancestors being visible or not, but it was not clear that the
            # property is apparently not effective immediately.
            if not component.isEnabled():
                break
            component_as_str = component.Text()
            if component_as_str.__len__() == 0:
                break
            contents.append(component_as_str)

        if contents.__len__() == 0:
            return "()"
        elif contents.__len__() == 1:
            return "(" + contents[0] + ",)"
        else:
            return "(" + ", ".join(contents) + ")"

    def Value(self) -> str:
        """
        Value cannot return a true value since there is no indication of the sequence elements type
        Cannot be done using: class.Value = class.Text since the Text method is added to instances, not to the class
        """
        return self.Text()


def _AdjustComponents(
    components: Sequence[text_wgt_t, ...],
    length: int,
) -> None:
    """"""
    for c_idx, component in enumerate(components):
        if c_idx < length:
            component.setVisible(True)
            component.setEnabled(True)
        else:
            component.setVisible(False)
            component.setEnabled(False)

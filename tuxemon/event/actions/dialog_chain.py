#
# Tuxemon
# Copyright (c) 2014-2017 William Edwards <shadowapex@gmail.com>,
#                         Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import annotations
import logging

from tuxemon.locale import replace_text
from tuxemon.event.eventaction import EventAction
from tuxemon.tools import open_dialog
from tuxemon.graphics import get_avatar
from typing import NamedTuple, final, Optional
from tuxemon.states.dialog import DialogState
from tuxemon.sprite import Sprite
import warnings

logger = logging.getLogger(__name__)


class DialogChainActionParameters(NamedTuple):
    text: str
    avatar: str


@final
class DialogChainAction(EventAction[DialogChainActionParameters]):
    """
    Open a dialog and waits.

    Other dialog chains will add text to the dialog
    without closing it. Dialog chains must be ended with the ${{end}} keyword.

    You may also use special variables in dialog events. Here is a list of
    available variables:

    * ${{name}} - The current player's name.
    * ${{end}} - Ends the dialog chain.

    Script usage:
        .. code-block::

            dialog_chain <text>,<avatar>

    Script parameters:
        text: Text of the dialog.
        avatar: Monster avatar. If it is a number, the monster is the
            corresponding monster slot in the player's party.
            If it is a string, we're referring to a monster by name.

    """

    name = "dialog_chain"
    param_class = DialogChainActionParameters

    def start(self) -> None:
        warnings.warn(
            f"Found deprecated dialog_chain action, please use "
            f"translated_dialog_chain instead. "
            f"Action: {self.name}. "
            f"Parameters: {self.raw_parameters}.",
            DeprecationWarning,
        )

        # hack to allow unescaped commas in the dialog string
        text = ", ".join(self.raw_parameters)
        text = replace_text(self.session, text)

        # If text is "${{end}}, then close the current dialog
        if not text == "${{end}}":
            self.stop()

            # is a dialog already open?
            try:
                dialog = self.session.client.get_state_by_name(DialogState)
                # yes, so just add text to it
                dialog.text_queue.append(text)
            except ValueError:
                # no, so create new dialog with this line
                avatar = get_avatar(self.session, self.parameters.avatar)
                self.open_dialog(text, avatar)

    def update(self) -> None:
        # hack to allow unescaped commas in the dialog string
        text = ", ".join(self.raw_parameters)
        if text == "${{end}}":
            try:
                self.session.client.get_state_by_name(DialogState)
            except ValueError:
                self.stop()

    def open_dialog(self, initial_text: str, avatar: Optional[Sprite]) -> None:
        logger.info("Opening chain dialog window")
        open_dialog(self.session, [initial_text], avatar)

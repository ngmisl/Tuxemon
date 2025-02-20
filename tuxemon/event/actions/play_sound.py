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
from tuxemon import audio
from tuxemon.event.eventaction import EventAction
from typing import NamedTuple, final


class PlaySoundActionParameters(NamedTuple):
    filename: str


@final
class PlaySoundAction(EventAction[PlaySoundActionParameters]):
    """
    Play a sound from "resources/sounds/".

    Script usage:
        .. code-block::

            play_sound <filename>

    Script parameters:
        filename: Sound file to load.

    """

    name = "play_sound"
    param_class = PlaySoundActionParameters

    def start(self) -> None:
        filename = self.parameters.filename
        sound = audio.load_sound(filename)
        sound.play()

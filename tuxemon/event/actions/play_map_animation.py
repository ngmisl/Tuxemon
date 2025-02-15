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

from tuxemon import prepare
from tuxemon.event.eventaction import EventAction
from tuxemon.graphics import load_animation_from_frames
from typing import NamedTuple, Union, final
from tuxemon.states.world.worldstate import WorldState

logger = logging.getLogger(__name__)


class PlayMapAnimationActionParameters(NamedTuple):
    animation_name: str
    duration: float
    loop: str
    tile_pos_x: Union[int, str]
    tile_pos_y: Union[int, None]


@final
class PlayMapAnimationAction(EventAction[PlayMapAnimationActionParameters]):
    """
    Play a map animation at a given position in the world map.

    Script usage:
        .. code-block::

            play_map_animation <animation_name> <duration> <loop> "player"
            play_map_animation <animation_name> <duration> <loop> <tile_pos_x> <tile_pos_y>

    Script parameters:
        animation_name: The name of the animation stored under
            resources/animations/tileset. For example, an animation called
            "grass" will load frames called "grass.xxx.png".
        duration: The duration of each frame of the animation in seconds.
        loop: Can be either "loop" or "noloop" to loop the animation.
        tile_pos: Can be either an x,y coordinate or "player" to draw the
            animation at the player's location.

    """

    name = "play_map_animation"
    param_class = PlayMapAnimationActionParameters

    def start(self) -> None:
        # ('play_animation', 'grass,1.5,noloop,player', '1', 6)
        # "position" can be either a (x, y) tile coordinate or "player"
        animation_name = self.parameters.animation_name
        duration = self.parameters.duration
        directory = prepare.fetch("animations", "tileset")

        if self.parameters.loop == "loop":
            loop = True
        elif self.parameters.loop == "noloop":
            loop = False
        else:
            logger.error('animation loop value must be "loop" or "noloop"')
            raise ValueError

        # Check to see if this animation has already been loaded.
        # If it has, play the animation.
        world_state = self.session.client.get_state_by_name(WorldState)

        # Determine the tile position where to draw the animation.
        # TODO: unify npc/player sprites and map animations
        if self.parameters[3] == "player":
            position = self.session.player.tile_pos
        else:
            assert self.parameters.tile_pos_y
            position = (
                int(self.parameters.tile_pos_x),
                int(self.parameters.tile_pos_y),
            )

        animations = world_state.map_animations
        if animation_name in animations:
            animations[animation_name]["position"] = position
            animations[animation_name]["animation"].play()

        else:
            # Not loaded already, so load it...
            animation = load_animation_from_frames(
                directory,
                animation_name,
                duration,
                loop,
            )

            animations[animation_name] = {
                "animation": animation,
                "position": position,
                "layer": 4,
            }

            animation.play()

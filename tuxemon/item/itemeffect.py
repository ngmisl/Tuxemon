#
# Tuxemon
# Copyright (C) 2014, William Edwards <shadowapex@gmail.com>,
#                     Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon.
#
# Tuxemon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tuxemon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tuxemon.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributor(s):
#
# William Edwards <shadowapex@gmail.com>
# Leif Theden <leif.theden@gmail.com>
# Andy Mender <andymenderunix@gmail.com>
# Adam Chevalier <chevalieradam2@gmail.com>
#
# item Item handling module.
#
#

from __future__ import annotations
import logging

from tuxemon.tools import NamedTupleProtocol, cast_parameters_to_namedtuple
from typing import TypeVar, Generic, ClassVar, Type, Sequence, Any, TypedDict,\
    TYPE_CHECKING
from tuxemon.session import Session

if TYPE_CHECKING:
    from tuxemon.npc import NPC
    from tuxemon.monster import Monster

logger = logging.getLogger(__name__)

ParameterClass = TypeVar("ParameterClass", bound=NamedTupleProtocol)


class ItemEffectResult(TypedDict):
    success: bool


class ItemEffect(Generic[ParameterClass]):
    """ItemEffects are executed by items.

    ItemEffect subclasses implement "effects" defined in Tuxemon items.
    All subclasses, at minimum, must implement the following:

    * The ItemEffect.apply() method
    * A meaningful name, which must match the name in item file effects

    By populating the "valid_parameters" class attribute, subclasses
    will be assigned a "parameters" instance attribute that holds the
    parameters passed to the action in the item file.  It is also used
    to check the syntax of effects, by verifying the correct type and
    number of parameters passed.

    Parameters
    ==========

    Tuxemon supports type-checking of the parameters defined in the items.

    valid_parameters may be the following format (may change):

    (type, name)

    * the type may be any valid python type, or even a python class or function
    * type may be a single type, or a tuple of types
    * type, if a tuple, may include None is indicate the parameter is optional
    * name must be a valid python string

    After parsing the parameters of the Item, the parameter's value
    will be passed to the type constructor.

    Example types: str, int, float, Monster, NPC

    (int, "duration")                => duration must be an int
    ((int, float), "duration")       => can be an int or float
    ((int, float, None), "duration") => is optional

    (Monster, "monster_slug")   => a Monster instance will be created
    """

    name: ClassVar[str] = "GenericEffect"
    param_class: ClassVar[Type[ParameterClass]]

    def __init__(
        self,
        session: Session,
        user: NPC,
        parameters: Sequence[Any],
    ) -> None:

        self.session = session
        self.user = user

        # if you need the parameters before they are processed, use this
        self.raw_parameters = parameters

        # parse parameters
        try:
            if self.param_class._fields:

                # cast the parameters to the correct type, as defined in cls.valid_parameters
                self.parameters = cast_parameters_to_namedtuple(
                    parameters,
                    self.param_class,
                )
            else:
                self.parameters = parameters

        except ValueError:
            logger.error(f"error while parsing for {self.name}")
            logger.error(f"cannot parse parameters: {parameters}")
            logger.error(self.param_class)
            logger.error("please check the parameters and verify they are correct")
            self.parameters = None

        self._done = False

    def apply(self, target: Monster) -> ItemEffectResult:
        pass

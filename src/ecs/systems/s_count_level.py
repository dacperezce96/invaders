from typing import List
import esper
import pygame
from src.ecs.components.c_changing_text import CChangingText

from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator

def system_count_flags(world:esper.World, flags:List[CSurface], num:int, ent:int):
    text_change = world.component_for_entity(ent, CChangingText)
    text_change.text = str(num).zfill(2)
    if num > 5:
        flags[5].visible = True
        flags[4].visible = False
        flags[3].visible = False
        flags[2].visible = False
        flags[1].visible = False
        flags[0].visible = True
    elif num > 4:
        flags[5].visible = False
        flags[4].visible = True
        flags[3].visible = True
        flags[2].visible = True
        flags[1].visible = True
        flags[0].visible = True
    elif num > 3:
        flags[5].visible = False
        flags[4].visible = False
        flags[3].visible = True
        flags[2].visible = True
        flags[1].visible = True
        flags[0].visible = True
    elif num > 2:
        flags[5].visible = False
        flags[4].visible = False
        flags[3].visible = False
        flags[2].visible = True
        flags[1].visible = True
        flags[0].visible = True
    elif num > 1:
        flags[5].visible = False
        flags[4].visible = False
        flags[3].visible = False
        flags[2].visible = False
        flags[1].visible = True
        flags[0].visible = True
    elif num > 0:
        flags[5].visible = False
        flags[4].visible = False
        flags[3].visible = False
        flags[2].visible = False
        flags[1].visible = False
        flags[0].visible = True
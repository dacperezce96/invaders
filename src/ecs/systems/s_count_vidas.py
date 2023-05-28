from typing import List
import esper
import pygame

from src.ecs.components.c_surface import CSurface

def system_count_vidas(world:esper.World, vidas:List[CSurface], num:int):
    if num > 3:
        vidas[2].visible = True
        vidas[1].visible = True
        vidas[0].visible = True
    elif num > 2:
        vidas[2].visible = False
        vidas[1].visible = True
        vidas[0].visible = True
    elif num > 1:
        vidas[2].visible = False
        vidas[1].visible = False
        vidas[0].visible = True
    elif num > 0:
        vidas[2].visible = False
        vidas[1].visible = False
        vidas[0].visible = False

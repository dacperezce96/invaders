import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_move_up import CMoveUp

def system_move_up(world: esper.World, now:bool):
    components = world.get_components(CTransform, CVelocity, CMoveUp)
    for entity, (c_t, c_v, c_m) in components:
        if now:
            c_t.pos.y = c_m.final_high
            c_v.vel =  pygame.Vector2(0,0)
        elif c_t.pos.y - c_m.final_high < 1:
            c_t.pos.y = c_m.final_high
            c_v.vel =  pygame.Vector2(0,0)
            now = True
    if now:
        return True
    else:
        return False    
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_move_up import CMoveUp
from src.ecs.components.tags.c_tag_star import CTagStar

def system_star_loop(world: esper.World, max_heigh:int):
    components = world.get_components(CTransform, CTagStar)
    for entity, (c_t, c_m) in components:
        if c_t.pos.y > max_heigh:
            c_t.pos.y = 0
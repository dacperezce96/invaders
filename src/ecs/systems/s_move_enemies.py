from typing import List
import  pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemie import CTagEnemie
from src.ecs.components.tags.c_tag_guia import CTagGuia
from src.engine.service_locator import ServiceLocator

def system_move_enemies(world:esper.World, enemie_ent:List[int]):
    componets = world.get_components(CTransform, CVelocity, CSurface, CTagGuia)
    c_t:CTransform
    c_s:CSurface
    c_v:CVelocity
    max_travel = 25
    for entity, (c_t, c_v, c_s, c_e) in componets:
        pos_ini = 0
        if c_t.pos.x < pos_ini - max_travel:
            c_v.vel.x *= -1
            c_t.pos.x = (pos_ini - max_travel)
        elif c_t.pos.x > pos_ini + max_travel:
            c_v.vel.x *= -1
            c_t.pos.x = (pos_ini + max_travel)
        for enemy in enemie_ent:
            e_t = world.component_for_entity(enemy, CTransform)
            e_p = world.component_for_entity(enemy, CTagEnemie)
            e_t.pos.x = e_p.pos.x + c_t.pos.x


